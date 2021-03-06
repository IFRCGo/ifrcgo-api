import factory
from factory import fuzzy
import datetime
import pytz

from .. import models


class RegionalProjectFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.RegionalProject

    name = fuzzy.FuzzyText(length=50, prefix='regional-project-')
    created_at = fuzzy.FuzzyDateTime(datetime.datetime(2008, 1, 1, tzinfo=pytz.utc))
    modified_at = fuzzy.FuzzyDateTime(datetime.datetime(2008, 1, 1, tzinfo=pytz.utc))
