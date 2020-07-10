import sys
import os
import json
from django.core.management.base import BaseCommand, CommandError
from django.contrib.gis.utils import LayerMapping
from django.contrib.gis.gdal import DataSource
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.geos import MultiPolygon
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from api.models import Country
from api.models import Region

class Command(BaseCommand):
  help = "import a shapefile of adminstrative boundary level 0 data to the GO database. To run, python manage.py import-admin0-data input.shp"

  missing_args_message = "Filename is missing. A shapefile with valid admin polygons is required."

  def add_arguments(self, parser):
    parser.add_argument('filename', nargs='+', type=str)
    parser.add_argument(
      '--update-bbox',
      action='store_true',
      help='Update the bbox of the country geometry. Used if you want to overwrite changes that are made by users via the Django Admin'
      )
    parser.add_argument(
      '--update-centroid',
      action='store_true',
      help='Update the centroid of the country geometry. Used if you want to overwrite changes that are made by users via the Django Admin'
      )

  @transaction.atomic
  def handle(self, *args, **options):
    filename = options['filename'][0]

    region_enum = {
      'Africa': 0,
      'Americas': 1,
      'Asia-Pacific': 2,
      'Europe': 3,
      'Middle East and North Africa': 4
    }

    try:
      data = DataSource(filename)
    except:
      raise CommandError('Could not open file')

    # first, let's import all the geometries for countries with iso code
    for feature in data[0]:
      feature_iso2 = feature.get('ISO2').lower()
      if feature_iso2:
        geom_wkt = feature.geom.wkt
        geom = GEOSGeometry(geom_wkt, srid=4326)
        if (geom.geom_type == 'Polygon'):
          geom = MultiPolygon(geom)

        centroid = geom.centroid.wkt
        bbox = geom.envelope.geojson

        # find this country in the database
        try:
          country = Country.objects.get(iso=feature_iso2, record_type=1)
          # if the country exist
          # add geom
          country.geom = geom.wkt

          if options['update_bbox']:
            # add bbox
            country.bbox = bbox

          if options['update_centroid']:
            # add centroid
            country.centroid = centroid

          # save
          print('updating %s with geometries' %feature_iso2)
          country.save()
        except ObjectDoesNotExist:
          print('adding missing country', feature_iso2)

          # new country object
          country = Country()

          name = feature.get('NAME_ICRC')
          record_type = 1 # country
          iso = feature_iso2
          iso3 = feature.get('ISO3').lower()
          region = feature.get('REGION_IFR')

          # get region from db
          region_id = Region.objects.get(name=region_enum[region])

          country.name = name
          country.record_type = 1
          country.iso = iso
          country.iso3 = iso3
          country.region = region_id
          country.geom = geom.wkt
          country.centroid = centroid
          country.bbox = bbox

          # save
          country.save()
    
      print('done!')



