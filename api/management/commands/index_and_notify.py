from datetime import datetime, timezone, timedelta
from django.db.models import Q
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.conf import settings
from django.template.loader import render_to_string
from elasticsearch.helpers import bulk
from api.indexes import ES_PAGE_NAME
from api.esconnection import ES_CLIENT
from api.models import Country, Appeal, Event, FieldReport
from api.logger import logger
from notifications.models import RecordType, SubscriptionType, Subscription
from notifications.hello import get_hello
from notifications.notification import send_notification
from main.frontend import frontend_url
import html

time_interval = timedelta(minutes = 5)
time_interva2 = timedelta(   days = 1) # to check: the change was not between time_interval and time_interva2, so that the user don't receive email more frequent than a day.

events_sent_to = {} # to document sent events before re-sending them via specific following

class Command(BaseCommand):
    help = 'Index and send notificatins about recently changed records'

    def get_time_threshold(self):
        return datetime.utcnow().replace(tzinfo=timezone.utc) - time_interval

    def get_time_threshold2(self):
        return datetime.utcnow().replace(tzinfo=timezone.utc) - time_interva2


    def gather_country_and_region(self, records):
        # Appeals only, since these have a single country/region
        countries = []
        regions = []
        for record in records:
            if record.country is not None:
                countries.append('c%s' % record.country.id)
                if record.country.region is not None:
                    regions.append('r%s' % record.country.region.id)
        countries = list(set(countries))
        regions = list(set(regions))
        return countries, regions


    def gather_countries_and_regions(self, records):
        # Applies to emergencies and field reports, which have a
        # many-to-many relationship to countries and regions
        countries = []
        for record in records:
            if record.countries is not None:
                countries += [country.id for country in record.countries.all()]
        countries = list(set(countries))
        qs = Country.objects.filter(pk__in=countries)
        regions = ['r%s' % country.region.id for country in qs if country.region is not None]
        countries = ['c%s' % id for id in countries]
        return countries, regions


    def gather_subscribers(self, records, rtype, stype):
        # Gather the email addresses of users who should be notified
        # Start with any users subscribed directly to this record type.
        subscribers = User.objects.filter(subscription__rtype=rtype, subscription__stype=stype, is_active=True).values('email')

        # For FOLLOWED_EVENTs we do not collect other generic (d*, country, region) subscriptions, just one. This part is not called.
        if (rtype != RecordType.FOLLOWED_EVENT):
            dtypes = list(set(['d%s' % record.dtype.id for record in records if record.dtype is not None]))

            if (rtype == RecordType.APPEAL):
                countries, regions = self.gather_country_and_region(records)
            else:
                countries, regions = self.gather_countries_and_regions(records)

            lookups = dtypes + countries + regions
            if len(lookups):
                subscribers = (subscribers | User.objects.filter(subscription__lookup_id__in=lookups, is_active=True).values('email')).distinct()
        emails = [subscriber['email'] for subscriber in subscribers]
        return emails


    def get_template(self):
        return 'email/generic_notification.html'
        #new will be: return 'design/generic_notification.html'


    # Get the front-end url of the resource
    def get_resource_uri (self, record, rtype):
        # Determine the front-end URL
        resource_uri = frontend_url
        if rtype == RecordType.APPEAL and (
                record.event is not None and not record.needs_confirmation):
            # Appeals with confirmed emergencies link to that emergency
            resource_uri = '%s/emergencies/%s' % (frontend_url, record.event.id)
        elif rtype != RecordType.APPEAL:
            # Field reports and (one-by-one followed or globally subscribed) emergencies
            resource_uri = '%s/%s/%s' % (
                frontend_url,
                'emergencies' if rtype == RecordType.EVENT or rtype == RecordType.FOLLOWED_EVENT else 'reports',
                record.id
            )
        return resource_uri


    def get_admin_uri (self, record, rtype):
        admin_page = {
            RecordType.FIELD_REPORT: 'fieldreport',
            RecordType.APPEAL: 'appeal',
            RecordType.EVENT: 'event',
            RecordType.FOLLOWED_EVENT: 'event',
        }[rtype]
        return 'https://%s/admin/api/%s/%s/change' % (
            settings.BASE_URL,
            admin_page,
            record.id,
        )


    def get_record_title(self, record, rtype):
        if rtype == RecordType.FIELD_REPORT:
            sendMe = record.summary
            if record.countries.all():
                country = record.countries.all()[0].name
                if country not in sendMe:
                    sendMe = sendMe + ' (' + country + ')'
            return sendMe
        else:
            return record.name

    def get_record_content(self, record, rtype):
        if rtype == RecordType.FIELD_REPORT:
            sendMe = record.description
        elif rtype == RecordType.APPEAL:
            sendMe = record.sector
            if record.code:
                sendMe += ', ' + record.code
        elif rtype == RecordType.EVENT or rtype == RecordType.FOLLOWED_EVENT:
            sendMe = record.summary
        else:
            sendMe = '?'
        return html.unescape(sendMe) # For contents we allow HTML markup. = autoescape off in generic_notification.html template.


    def get_record_display(self, rtype, count):
        display = {
            RecordType.FIELD_REPORT: 'field report',
            RecordType.APPEAL: 'appeal',
            RecordType.EVENT: 'event',
            RecordType.FOLLOWED_EVENT: 'event',
        }[rtype]
        if (count > 1):
            display += 's'
        return display


    def notify(self, records, rtype, stype):
        record_count = records.count()
        if not record_count:
            return
        emails = self.gather_subscribers(records, rtype, stype)
        if not len(emails):
            return

        # Only serialize the first 10 records
        entries = list(records) if record_count <= 10 else list(records[:10])
        record_entries = []
        for record in entries:
            record_entries.append({
                'resource_uri': self.get_resource_uri(record, rtype),
                'admin_uri': self.get_admin_uri(record, rtype),
                'title': self.get_record_title(record, rtype),
                'content': self.get_record_content(record, rtype),
            })

        template_path = self.get_template()
        html = render_to_string(template_path, {
            'hello': get_hello(),
            'count': record_count,
            'records': record_entries,
            'is_staff': True, # TODO: fork the sending to "is_staff / not ~" groups
        })
        recipients = emails
        adj = 'New' if stype == SubscriptionType.NEW else 'Modified'
        record_type = self.get_record_display(rtype, record_count)
        subject = '%s %s %s(s) in IFRC GO ' % (
            record_count,
            adj,
            record_type,
        )

        # For new (email-documented :10) events we store data to events_sent_to{ event_id: recipients }
        if stype == SubscriptionType.EDIT:
            for e in list(records.values('id'))[:10]:
                i = e['id']
                if i not in events_sent_to:
                    events_sent_to[i] = []
                email_list_to_add = list(set(events_sent_to[i] + recipients))
                if email_list_to_add:
                    events_sent_to[i] = list(filter(None, email_list_to_add)) # filter to skip empty elements

        logger.info('Notifying %s subscriber(s) about %s %s %s' % (len(emails), record_count, adj.lower(), record_type))
        send_notification(subject, recipients, html)

#   Almost code duplication - usually run for 1 person, but the syntax kept the plurals:
    def notify_personal(self, records, rtype, stype, uid):
        record_count = records.count()
        if not record_count:
            return
        users = User.objects.filter(pk=uid, is_active=True)
        if not len(users):
            return
        else:
            emails = [users.values('email')[0]['email']]  # It is only one email in this case

        # Only serialize the first 10 records
        entries = list(records) if record_count <= 10 else list(records[:10])
        record_entries = []
        for record in entries:
            record_entries.append({
                'resource_uri': self.get_resource_uri(record, rtype),
                'admin_uri': self.get_admin_uri(record, rtype),
                'title': self.get_record_title(record, rtype),
                'content': self.get_record_content(record, rtype),
            })
        is_staff = users.values('is_staff')[0]['is_staff']
        template_path = self.get_template()
        html = render_to_string(template_path, {
            'hello': get_hello(),
            'count': record_count,
            'records': record_entries,
            'is_staff': is_staff,
        })
        recipients = emails
        adj = '' if stype == SubscriptionType.NEW else ''
        record_type = self.get_record_display(rtype, record_count)
        subject = '%s %s %s(s) in IFRC GO ' % (
            record_count,
            adj,
            record_type,
        )
        if len(recipients):
            # check if email is not in events_sent_to{event_id: recipients}
            if not emails:
                logger.info('Silent about %s one-by-one subscribed %s – user has not set email address' % (adj.lower(), record_type))
            elif (records[0].id not in events_sent_to) or (emails[0] not in events_sent_to[records[0].id]):
                logger.info('Notifying %s subscriber about %s %s one-by-one subscribed %s' % (len(emails), record_count, adj.lower(), record_type))
                send_notification(subject, list(recipients), html)
            else:
                logger.info('Silent about %s one-by-one subscribed %s – user already notified via generic subscription' % (adj.lower(), record_type))


    def index_new_records(self, records):
        self.bulk([self.convert_for_bulk(record, create=True) for record in list(records)])


    def index_updated_records(self, records):
        self.bulk([self.convert_for_bulk(record, create=False) for record in list(records)])


    def convert_for_bulk(self, record, create):
        data = record.indexing()
        metadata = {
            '_op_type': 'create' if create else 'update',
            '_index': ES_PAGE_NAME,
            '_type': 'page',
            '_id': record.es_id()
        }
        if (create):
            metadata.update(**data)
        else:
            metadata['doc'] = data
        return metadata


    def bulk(self, actions):
        try:
            created, errors = bulk(client=ES_CLIENT , actions=actions)
            if len(errors):
                logger.error('Produced the following errors:')
                logger.error('[%s]' % ', '.join(map(str, errors)))
        except Exception as e:
            logger.error('Could not index records')
            logger.error('%s...' % str(e)[:512])


    # Remove items in a queryset where updated_at == created_at.
    # This leaves us with only ones that have been modified.
    def filter_just_created(self, queryset):
        if queryset.first() is None:
            return []
        if hasattr(queryset.first(), 'modified_at') and queryset.first().modified_at is not None:
            return [record for record in queryset if (
                record.modified_at.replace(microsecond=0) == record.created_at.replace(microsecond=0))]
        else:
            return [record for record in queryset if (
                record.updated_at.replace(microsecond=0) == record.created_at.replace(microsecond=0))]


    def handle(self, *args, **options):
        t = self.get_time_threshold()
        t2 = self.get_time_threshold2()

        cond1 = Q(created_at__gte=t)
        condU = Q(updated_at__gte=t)
        condR = Q(real_data_update__gte=t) # instead of modified at
        cond2 = Q(previous_update__gte=t2) # we negate thes, so we want: no previous_update in the last day. So: send 1-ce a day!

        new_reports = FieldReport.objects.filter(cond1)
        updated_reports = FieldReport.objects.filter(condU & ~cond2)

        new_appeals = Appeal.objects.filter(cond1)
        updated_appeals = Appeal.objects.filter(condR & ~cond2)

        new_events = Event.objects.filter(cond1)
        updated_events = Event.objects.filter(condU & ~cond2)

        followed_eventparams = Subscription.objects.filter(event_id__isnull=False)
        #followed_events = Event.objects.filter(updated_at__gte=t, pk__in=[x.event_id for x in followed_eventparams])

        #self.notify(new_reports, RecordType.FIELD_REPORT, SubscriptionType.NEW)
        self.notify(updated_reports, RecordType.FIELD_REPORT, SubscriptionType.EDIT)

        self.notify(new_appeals, RecordType.APPEAL, SubscriptionType.NEW)
        #self.notify(updated_appeals, RecordType.APPEAL, SubscriptionType.EDIT)

        self.notify(new_events, RecordType.EVENT, SubscriptionType.NEW)
        self.notify(updated_events, RecordType.EVENT, SubscriptionType.EDIT)

        for p in followed_eventparams:
            cond3 = Q(pk=p.event_id)
            followed_events = Event.objects.filter(condU & ~cond2 & cond3)
            if len(followed_events):
                self.notify_personal(followed_events, RecordType.FOLLOWED_EVENT, SubscriptionType.NEW, p.user_id)

        logger.info('Indexing %s updated field reports' % updated_reports.count())
        self.index_updated_records(self.filter_just_created(updated_reports))
        logger.info('Indexing %s updated appeals' % updated_appeals.count())
        self.index_updated_records(self.filter_just_created(updated_appeals))
        logger.info('Indexing %s updated events' % updated_events.count())
        self.index_updated_records(self.filter_just_created(updated_events))

        logger.info('Indexing %s new field reports' % new_reports.count())
        self.index_new_records(new_reports)
        logger.info('Indexing %s new appeals' % new_appeals.count())
        self.index_new_records(new_appeals)
        logger.info('Indexing %s new events' % new_events.count())
        self.index_new_records(new_events)
