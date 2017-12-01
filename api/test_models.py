from django.test import TestCase
from django.contrib.auth.models import User

import api.models as models


class DisasterTypeTest(TestCase):

    fixtures = ['DisasterTypes']

    def test_disaster_type_data(self):
        objs = models.DisasterType.objects.all()
        self.assertEqual(len(objs), 25)


class EventTest(TestCase):
    def setUp(self):
        models.Event.objects.create(name='disaster1', summary='test disaster')
        models.Event.objects.create(name='disaster2', summary='another test disaster')

    def test_disaster_create(self):
        obj1 = models.Event.objects.get(name='disaster1')
        obj2 = models.Event.objects.get(name='disaster2')
        self.assertEqual(obj1.summary, 'test disaster')
        self.assertEqual(obj2.summary, 'another test disaster')


class CountryTest(TestCase):

    fixtures = ['Countries']

    def test_country_data(self):
        objs = models.Country.objects.all()
        self.assertEqual(objs.count(), 260)


class ProfileTest(TestCase):
    def setUp(self):
        user = User.objects.create(username='username', first_name='pat', last_name='smith', password='password')
        user.profile.org = 'org'
        user.profile.save()

    def test_profile_create(self):
        profile = models.Profile.objects.get(user__username='username')
        self.assertEqual(profile.org, 'org')


"""
class AppealTest(TestCase):
    def setUp(self):
        event = models.Event.objects.create(name='disaster1', summary='test disaster')
        country = models.Country.objects.create(name='country')
        models.Appeal.objects.create(aid='test1', disaster=event, country=country)

    def test_appeal_create(self):
        event = models.Event.objects.get(name='disaster1')
        self.assertEqual(event.countries(), ['country'])
        country = models.Country.objects.get(name='country')
        obj = models.Appeal.objects.get(aid='test1')
        self.assertEqual(obj.aid, 'test1')
        self.assertEqual(obj.country, country)
        self.assertEqual(obj.event, event)
"""

class FieldReportTest(TestCase):

    fixtures = ['DisasterTypes']

    def setUp(self):
        event = models.Event.objects.create(name='disaster1', summary='test disaster')
        country = models.Country.objects.create(name='country')
        dtype = models.DisasterType.objects.get(pk=1)
        report = models.FieldReport.objects.create(rid='test1', event=event, dtype=dtype)
        report.countries.add(country)

    def test_field_report_create(self):
        event = models.Event.objects.get(name='disaster1')
        self.assertEqual(event.countries(), ['country'])
        country = models.Country.objects.get(name='country')
        obj = models.FieldReport.objects.get(rid='test1')
        self.assertEqual(obj.rid, 'test1')
        self.assertEqual(obj.countries.all()[0], country)
        self.assertEqual(obj.event, event)


class ServiceTest(TestCase):
    def setUp(self):
        models.Service.objects.create(name='test1', location='earth')
        models.Service.objects.create(name='test2', deployed=True, location='iceland')

    def test_service_create(self):
        obj1 = models.Service.objects.get(name='test1')
        self.assertFalse(obj1.deployed)
        self.assertEqual(obj1.location, 'earth')
        obj1 = models.Service.objects.get(name='test2')
        self.assertTrue(obj1.deployed)
        self.assertEqual(obj1.location, 'iceland')


class ProfileTest(TestCase):
    def setUp(self):
        user = User.objects.create(username='test1', password='12345678!')
        user.profile.department = 'testdepartment'
        user.save()

    def test_profile_create(self):
        obj = models.Profile.objects.get(user__username='test1')
        self.assertEqual(obj.department, 'testdepartment')
