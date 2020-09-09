[![Waffle.io - Columns and their card count](https://badge.waffle.io/IFRCGo/go-infrastructure.svg?columns=all)](https://waffle.io/IFRCGo/go-infrastructure)

[![CircleCI](https://circleci.com/gh/IFRCGo/go-api.svg?style=svg&circle-token=4337c3da24907bbcb5d6aa06f0d60c5f27845435)](https://circleci.com/gh/IFRCGo/go-api)

# IFRC GO API

## Staff email domains

A list of staff email domains, which the API will treat as single-validation,
email-verification only, is to be found
[here](https://github.com/IFRCGo/go-api/blob/master/registrations/views.py#L25).

## Requirements

-   docker and docker-compose

## Local Development

### Setup

     $ docker-compose build
     $ docker-compose run --rm migrate
     $ docker-compose run --rm loaddata

### Running tests

     $ docker-compose run --rm test

### Making new migrations

     $ docker-compose run --rm makemigrations

### If there are conflicting migrations (only works if the migrations don't modify the same models)

     $ docker-compose run --rm makemigrations_merge

### Applying the last migration files to database

     $ docker-compose run --rm migrate

### Accessing python shell

     $ docker-compose run --rm shell

### Adding super user

     $ docker-compose run --rm createsuperuser

### Running server

     $ docker-compose run --rm --service-ports serve

Access the site at http://localhost:8000

### Install new dependencies

     $ docker-compose build

## Adding/Updating translations (Django static)

```bash
# Creation and upkeep language po files (for eg: fr)
python3 manage.py makemessages -l fr
# Creation and upkeep language po files (for eg: multiple languages)
python3 manage.py makemessages -l en -l es -l ar -l fr
# Updating current language po files
python3 manage.py makemessages -a
# Translate empty string of po files using AWS Translate (Requires valid AWS_TRANSLATE_* env variables)
python3 manage.py translate_po
# Compile po files
python3 manage.py compilemessages
```

## Note for Django Model translations

```
# Use this to copy the data from original field to it's default lanauage.
# For eg: if the field `name` is registred for translation then
# this command will copy value from `name` to `name_en` if en is the default language.
python manage.py update_translation_fields

# Auto translate values from default lang to other language
python manage.py translate_model
```

## Generate coverage report

     $ docker-compose run --rm coverage

## Documentation

Identify the function/class to modify from [main/urls.py](main/urls.py).

### Add function descriptions

Use [docstrings](https://www.python.org/dev/peps/pep-0257/) to add action
specific descriptions,

```
class CustomViewset(viewsets.ReadOnlyModelViewSet):
    """
    list:
    Description for list action of Custom.

    read:
    Description for read action of Custom.
    """
```

### Add field descriptions

Look for the **field** definition in the `CustomViewset` class or its attributes
like `CustomFilter`.

Add `help_text` attribute to the field definition.

```
variable_name = filters.NumberFilter(field_name='variable name', lookup_expr='exact', help_text='Description string for variable name.')
```

Django automatically generates description strings for **standard** fields like
`id` or `ordering`.

# Continuous Integration

[Circle-ci](https://circleci.com/gh/IFRCGo/go-api) handles continuous
integration.

## Release to Docker Hub

To release a new version to docker hub do the following:

-   Update `version` value in `main/__init__.py`
-   Create a new git tag with the same version
-   Commit and make a PR against master
-   The tagged version of the code is used to build a new docker image and is
    pushed to docker hub

# Deployment

`main/runserver.sh` is the entrypoint for deploying this API to a new
environment. It is also the default command specified in `Dockerfile`.
`main/runserver.sh` requires that environment variables corresponding to
database connection strings, FTP settings, and email settings, among others, be
set. Check the script for the specific variables in your environment.

## Deployment command

```(bash)
docker run -p 80:80 --env-file .env -d -t ifrcgo/go-api:{TAG_NUMBER}
```

## Comment for loading data

In `main/runserver.sh` the line containing the `loaddata` command is only necessary when creating a new database. In other cases it might be causing the conflict, so it is commented. 

# Management commands to update and import admin0 and admin1 data

There are two Django management commands that helps to work with ICRC admin0 and admin1 shapefiles. These commands should be used only when you want to update geometries, or import new ones from a shapefile. The structure of the shapefile is not very flexible, but can be adjusted easily in the scripts. 

## import-admin0-data
This management command is used for updating and importing admin0 shapefile. To run:
* `python manage.py import-admin0-data <filename.shp>`

The above command will generate a list of missing countries in the database based on the iso2 code to a file called `missing-countries.txt`. In case the script comes across any countries with duplicate iso code, these will be stored in `duplicate-countries.txt`

### Options available for the command
* `--update-geom` -- updates the geometry for all countries matched in the shapefile using the iso2 code.
* `--update-bbox` -- updates the bbox for all countries matched in the shapefile using the iso2 code.
* `--update-centroid` -- updates the centroid for all countries from a CSV. The CSV should have iso code, latitude and longitude. If a country is missing in the CSV, the geometric centroid will be used.
* `--import-missing missing-countries.txt` -- this will import countries for the iso2 mentioned in `missing-countries.txt` to the database. The file is the same format as generated by the default command.
* `--update-iso3 iso3.csv` -- this will import iso3 codes for all countries from a csv file. The file should have `iso2, iso3` columns
* `--update-independent` -- updates the independence status for the country from the shapefile.

## import-admin1-data
This management command is used for updating and importing admin1 shapefile. To run:
* `python manage.py import-admin1-data <filename.shp>`

The above command will generate a list of missing districts in the database based on the district code and name (in case there are more than one district with the same code) to a file called `missing-district.txt`

### Options available for the command
* `--update-geom` -- updates the geometry for all districts matched in the shapefile using the iso2 code.
* `--update-bbox` -- updates the bbox for all districts matched in the shapefile using the iso2 code.
* `--update-centroid` -- updates the centroid for all districts matched in the shapefile using the iso2 code.
* `--import-missing missing-districts.txt` -- this will import districts for the iso2 mentioned in `missing-districts.txt` to the database. The file is the same format as generated by the default command.
* `--import-all` -- this option is used to import all districts in the shapefile, if they don't have a code we can match against in the database.

## Update bbox for regions
Run `python manage.py update-region-bbox` to update the bbox for each region in the database.
