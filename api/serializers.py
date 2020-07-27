import json
from rest_framework import serializers
from django.contrib.auth.models import User

from lang.translation import TranslatedModelSerializerMixin
from .models import (
    DisasterType,

    Region,
    Country,
    District,
    CountryKeyFigure,
    RegionKeyFigure,
    CountrySnippet,
    RegionSnippet,
    CountryLink,
    RegionLink,
    CountryContact,
    RegionContact,

    KeyFigure,
    Snippet,
    EventContact,
    Event,
    SituationReportType,
    SituationReport,

    Appeal,
    AppealType,
    AppealDocument,

    Profile,

    FieldReportContact,
    ActionsTaken,
    Action,
    Source,
    FieldReport,
)
from notifications.models import Subscription


class DisasterTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DisasterType
        fields = ('name', 'summary', 'id',)


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ('name', 'id', 'region_name')


class CountryCsvSerializer(serializers.ModelSerializer):
    region = RegionSerializer()

    class Meta:
        model = Country
        fields = ('name', 'iso', 'iso3', 'society_name', 'society_url', 'region', 'overview', 'key_priorities',
                  'inform_score', 'id', 'url_ifrc', 'record_type',)


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ('name', 'iso', 'iso3', 'society_name', 'society_url', 'region', 'overview', 'key_priorities',
                  'inform_score', 'id', 'url_ifrc', 'record_type',)


class MiniCountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ('name', 'iso', 'iso3', 'society_name', 'id', 'record_type', 'region',)


class RegoCountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ('name', 'society_name', 'region', 'id',)


class NotCountrySerializer(serializers.ModelSerializer):  # fake serializer for a short data response for PER
    class Meta:
        model = Country
        fields = ('id',)


class DistrictSerializer(serializers.ModelSerializer):
    country = MiniCountrySerializer()

    class Meta:
        model = District
        fields = ('name', 'code', 'country', 'country_iso', 'country_name', 'id',)


class MiniDistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = ('name', 'code', 'country_iso', 'country_name', 'id', 'is_enclave',)


class RegionKeyFigureSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegionKeyFigure
        fields = ('region', 'figure', 'deck', 'source', 'visibility', 'id',)


class CountryKeyFigureSerializer(serializers.ModelSerializer):
    class Meta:
        model = CountryKeyFigure
        fields = ('country', 'figure', 'deck', 'source', 'visibility', 'id',)


class RegionSnippetCsvSerializer(serializers.ModelSerializer):
    region = RegionSerializer()

    class Meta:
        model = RegionSnippet
        fields = ('region', 'snippet', 'image', 'visibility', 'id',)


class RegionSnippetSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegionSnippet
        fields = ('region', 'snippet', 'image', 'visibility', 'id',)


class CountrySnippetCsvSerializer(serializers.ModelSerializer):
    country = CountrySerializer()

    class Meta:
        model = CountrySnippet
        fields = ('country', 'snippet', 'image', 'visibility', 'id',)


class CountrySnippetSerializer(serializers.ModelSerializer):
    class Meta:
        model = CountrySnippet
        fields = ('country', 'snippet', 'image', 'visibility', 'id',)


class RegionLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegionLink
        fields = ('title', 'url', 'id',)


class CountryLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = CountryLink
        fields = ('title', 'url', 'id',)


class RegionContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegionContact
        fields = ('ctype', 'name', 'title', 'email', 'id',)


class CountryContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = CountryContact
        fields = ('ctype', 'name', 'title', 'email', 'id',)


class RegionRelationSerializer(serializers.ModelSerializer):
    links = RegionLinkSerializer(many=True, read_only=True)
    contacts = RegionContactSerializer(many=True, read_only=True)
    class Meta:
        model = Region
        fields = ('links', 'contacts', 'name', 'id',)

class CountryRelationSerializer(serializers.ModelSerializer):
    links = CountryLinkSerializer(many=True, read_only=True)
    contacts = CountryContactSerializer(many=True, read_only=True)
    class Meta:
        model = Country
        fields = ('links', 'contacts', 'name', 'iso', 'society_name', 'society_url', 'region', 'overview', 'key_priorities', 'inform_score', 'id', 'url_ifrc',)

class RelatedAppealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appeal
        fields = ('aid', 'num_beneficiaries', 'amount_requested', 'amount_funded', 'status', 'start_date', 'id',)

class KeyFigureSerializer(serializers.ModelSerializer):
    class Meta:
        model = KeyFigure
        fields = ('number', 'deck', 'source', 'id',)

class SnippetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Snippet
        fields = ('event', 'snippet', 'image', 'visibility', 'position', 'tab', 'id',)

class EventContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventContact
        fields = ('ctype', 'name', 'title', 'email', 'phone', 'event', 'id',)

class FieldReportContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = FieldReportContact
        fields = ('ctype', 'name', 'title', 'email', 'phone', 'id',)


class MiniFieldReportSerializer(serializers.ModelSerializer):
    contacts = FieldReportContactSerializer(many=True)
    countries = MiniCountrySerializer(many=True)

    class Meta:
        model = FieldReport
        fields = (
            'summary', 'status', 'description', 'contacts', 'countries', 'created_at', 'updated_at', 'report_date', 'id', 'is_covid_report', 'visibility',
            'num_injured', 'num_dead', 'num_missing', 'num_affected', 'num_displaced', 'num_assisted', 'num_localstaff', 'num_volunteers', 'num_expats_delegates',
            'gov_num_injured', 'gov_num_dead', 'gov_num_missing', 'gov_num_affected', 'gov_num_displaced',  'gov_num_assisted',
            'other_num_injured', 'other_num_dead', 'other_num_missing', 'other_num_affected', 'other_num_displaced', 'other_num_assisted',
            'num_potentially_affected', 'gov_num_potentially_affected', 'other_num_potentially_affected', 'num_highest_risk', 'gov_num_highest_risk', 'other_num_highest_risk', 'affected_pop_centres', 'gov_affected_pop_centres', 'other_affected_pop_centres',
            'epi_cases', 'epi_suspected_cases', 'epi_probable_cases', 'epi_confirmed_cases', 'epi_num_dead', 'epi_figures_source',
        )

# The list serializer can include a smaller subset of the to-many fields.
# Also include a very minimal one for linking, and no other related fields.
class MiniEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('name', 'dtype', 'id', 'slug', 'parent_event',)


class ListMiniEventSerializer(serializers.ModelSerializer):
    dtype = DisasterTypeSerializer(read_only=True)

    class Meta:
        model = Event
        fields = ('id', 'name', 'slug', 'dtype', 'auto_generated_source')


class ListEventSerializer(serializers.ModelSerializer):
    appeals = RelatedAppealSerializer(many=True, read_only=True)
    countries = MiniCountrySerializer(many=True)
    field_reports = MiniFieldReportSerializer(many=True, read_only=True)
    dtype = DisasterTypeSerializer()

    class Meta:
        model = Event
        fields = ('name', 'dtype', 'countries', 'summary', 'num_affected', 'ifrc_severity_level', 'glide',
                  'disaster_start_date', 'created_at', 'auto_generated', 'appeals', 'is_featured', 'is_featured_region',
                  'field_reports', 'updated_at', 'id', 'slug', 'parent_event')

class ListEventCsvSerializer(serializers.ModelSerializer):
    appeals = serializers.SerializerMethodField()
    field_reports = serializers.SerializerMethodField()
    countries = serializers.SerializerMethodField()
    dtype = DisasterTypeSerializer()

    def get_countries(self, obj):
        country_fields = {}
        countries = obj.countries.all()
        if len(countries) > 0:
            country_fields['id'] = ', '.join([str(country.id) for country in countries])
            country_fields['name'] = ', '.join([str(country.name) for country in countries])
        else:
            country_fields['id'] = ''
            country_fields['name'] = ''
        return country_fields

    def get_field_reports(self, obj):
        field_reports_fields = {}
        field_reports = obj.field_reports.all()
        if len(field_reports) > 0:
            field_reports_fields['id'] = ', '.join([str(field_reports.id) for field_reports in field_reports])
        else:
            field_reports_fields['id'] = ''
        return field_reports_fields

    def get_appeals(self, obj):
        appeals_fields = {}
        appeals = obj.appeals.all()
        if len(appeals) > 0:
            appeals_fields['id'] = ', '.join([str(appeals.id) for appeals in appeals])
        else:
            appeals_fields['id'] = ''
        return appeals_fields

    class Meta:
        model = Event
        fields = ('name', 'dtype', 'countries', 'summary', 'num_affected', 'ifrc_severity_level', 'glide', 'disaster_start_date', 'created_at', 'auto_generated', 'appeals', 'is_featured', 'is_featured_region', 'field_reports', 'updated_at', 'id', 'slug', 'parent_event',)


class ListEventDeploymentsSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    type = serializers.CharField()
    deployments = serializers.IntegerField()


class DetailEventSerializer(serializers.ModelSerializer):
    appeals = RelatedAppealSerializer(many=True, read_only=True)
    contacts = EventContactSerializer(many=True, read_only=True)
    key_figures = KeyFigureSerializer(many=True, read_only=True)
    districts = MiniDistrictSerializer(many=True)
    countries = MiniCountrySerializer(many=True)
    field_reports = MiniFieldReportSerializer(many=True, read_only=True)

    class Meta:
        model = Event
        fields = ('name', 'dtype', 'countries', 'districts', 'summary', 'num_affected', 'ifrc_severity_level', 'glide', 'disaster_start_date', 'created_at', 'auto_generated', 'appeals', 'contacts', 'key_figures', 'is_featured', 'is_featured_region', 'field_reports', 'hide_attached_field_reports', 'updated_at', 'id', 'slug', 'tab_one_title', 'tab_two_title', 'tab_three_title', 'parent_event',)
        lookup_field = 'slug'


class SituationReportTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SituationReportType
        fields = ('type', 'id', 'is_primary',)


class SituationReportCsvSerializer(serializers.ModelSerializer):
    type = SituationReportTypeSerializer()
    event = MiniEventSerializer()

    class Meta:
        model = SituationReport
        fields = ('created_at', 'name', 'document', 'document_url', 'event', 'type', 'id', 'is_pinned', 'visibility',)


class SituationReportSerializer(serializers.ModelSerializer):
    type = SituationReportTypeSerializer()

    class Meta:
        model = SituationReport
        fields = ('created_at', 'name', 'document', 'document_url', 'event', 'type', 'id', 'is_pinned', 'visibility',)


class AppealCsvSerializer(serializers.ModelSerializer):
    country = MiniCountrySerializer()
    dtype = DisasterTypeSerializer()
    region = RegionSerializer()
    event = MiniEventSerializer()

    class Meta:
        model = Appeal
        fields = ('aid', 'name', 'dtype', 'atype', 'status', 'code', 'sector', 'num_beneficiaries', 'amount_requested',
                  'amount_funded', 'start_date', 'end_date', 'created_at', 'modified_at', 'event', 'needs_confirmation',
                  'country', 'region', 'id',)


class MiniAppealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appeal
        fields = ('name', 'id', 'code')


class AppealSerializer(serializers.ModelSerializer):
    country = MiniCountrySerializer()
    dtype = DisasterTypeSerializer()
    region = RegionSerializer()

    class Meta:
        model = Appeal
        fields = ('aid', 'name', 'dtype', 'atype', 'status', 'code', 'sector', 'num_beneficiaries', 'amount_requested',
                  'amount_funded', 'start_date', 'end_date', 'created_at', 'modified_at', 'event', 'needs_confirmation',
                  'country', 'region', 'id',)


class AppealDocumentCsvSerializer(serializers.ModelSerializer):
    appeal = MiniAppealSerializer()

    class Meta:
        model = AppealDocument
        fields = ('created_at', 'name', 'document', 'document_url', 'appeal', 'id',)


class AppealDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppealDocument
        fields = ('created_at', 'name', 'document', 'document_url', 'appeal', 'id',)

class ProfileSerializer(serializers.ModelSerializer):
    country = MiniCountrySerializer()
    class Meta:
        model = Profile
        fields = ('country', 'org', 'org_type', 'city', 'department', 'position', 'phone_number')

class MiniSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ('stype', 'rtype', 'country', 'region', 'event', 'dtype', 'lookup_id',)

class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()
    subscription = MiniSubscriptionSerializer(many=True)
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'profile', 'subscription', 'is_superuser',)

    def update(self, instance, validated_data):
        if 'profile' in validated_data:
            profile_data = validated_data.pop('profile')
            profile = Profile.objects.get(user=instance)
            profile.city = profile_data.get('city', profile.city)
            profile.org = profile_data.get('org', profile.org)
            profile.org_type = profile_data.get('org_type', profile.org_type)
            profile.department = profile_data.get('department', profile.department)
            profile.position = profile_data.get('position', profile.position)
            profile.phone_number = profile_data.get('phone_number', profile.phone_number)
            profile.country = profile_data.get('country', profile.country)
            profile.save()
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.save()
        return instance


class UserMeSerializer(UserSerializer):
    is_admin_for_countries = serializers.SerializerMethodField()
    is_admin_for_regions = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = UserSerializer.Meta.fields + ('is_admin_for_countries', 'is_admin_for_regions')

    def get_is_admin_for_countries(self, user):
        return set([
            int(permission[18:]) for permission in user.get_all_permissions()
            if ('api.country_admin_' in permission and permission[18:].isdigit())
        ])

    def get_is_admin_for_regions(self, user):
        return set([
            int(permission[17:]) for permission in user.get_all_permissions()
            if ('api.region_admin_' in permission and permission[17:].isdigit())
        ])


class ActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Action
        fields = ('name', 'id', 'organizations', 'field_report_types', 'category',)

class ActionsTakenSerializer(serializers.ModelSerializer):
    actions = ActionSerializer(many=True)
    class Meta:
        model = ActionsTaken
        fields = ('organization', 'actions', 'summary', 'id',)

class SourceSerializer(serializers.ModelSerializer):
    stype = serializers.SlugRelatedField(slug_field='name', read_only=True)
    class Meta:
        model = Source
        fields = ('stype', 'spec', 'id',)


class ListFieldReportSerializer(TranslatedModelSerializerMixin, serializers.ModelSerializer):
    countries = MiniCountrySerializer(many=True)
    dtype = DisasterTypeSerializer()
    event = MiniEventSerializer()
    actions_taken = ActionsTakenSerializer(many=True)

    class Meta:
        model = FieldReport
        fields = '__all__'


class ListFieldReportCsvSerializer(serializers.ModelSerializer):
    countries = serializers.SerializerMethodField()
    districts = serializers.SerializerMethodField()
    regions = serializers.SerializerMethodField()
    dtype = DisasterTypeSerializer()
    event = MiniEventSerializer()
    actions_taken = serializers.SerializerMethodField('get_actions_taken_for_organization')

    def get_countries(self, obj):
        country_fields = {
            'id': '',
            'name': ''
        }
        countries = obj.countries.all()
        if len(countries) > 0:
            country_fields['id'] = ', '.join([str(country.id) for country in countries])
            country_fields['name'] = ', '.join([str(country.name) for country in countries])
        return country_fields

    def get_districts(self, obj):
        district_fields = {
            'id': '',
            'name': ''
        }
        districts = obj.districts.all()
        if len(districts) > 0:
            district_fields['id'] = ', '.join([str(district.id) for district in districts])
            district_fields['name'] = ', '.join([str(district.name) for district in districts])
        return district_fields

    def get_regions(self, obj):
        region_fields = {
            'id': '',
            'region_name': ''
        }
        regions = obj.regions.all()
        if len(regions) > 0:
            region_fields['id'] = ', '.join([str(region.id) for region in regions])
            region_fields['region_name'] = ', '.join([str(region.region_name) for region in regions])
        return region_fields

    def get_actions_taken_for_organization(self, obj):
        actions_data = {}
        actions_taken = obj.actions_taken.all()
        for action in actions_taken:
            if action.organization not in actions_data:
                actions_data[action.organization] = []
            this_action = {
                'actions_name': [a.name for a in action.actions.all()],
                'actions_id': [a.id for a in action.actions.all()]
            }
            actions_data[action.organization] = {
                'action': json.dumps(this_action),
                'summary': action.summary
            }
        return actions_data

    class Meta:
        model = FieldReport
        fields = '__all__'


class DetailFieldReportSerializer(TranslatedModelSerializerMixin, serializers.ModelSerializer):
    user = UserSerializer()
    dtype = DisasterTypeSerializer()
    contacts = FieldReportContactSerializer(many=True)
    actions_taken = ActionsTakenSerializer(many=True)
    sources = SourceSerializer(many=True)
    event = MiniEventSerializer()
    countries = MiniCountrySerializer(many=True)
    districts = MiniDistrictSerializer(many=True)
    class Meta:
        model = FieldReport
        fields = '__all__'

class CreateFieldReportSerializer(TranslatedModelSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = FieldReport
        fields = '__all__'
