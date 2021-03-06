# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-16 22:26
from __future__ import unicode_literals
from django.db import migrations
from intake.constants import Counties

from project.migration_utils import FixtureDataMigration


class AddDefaultCounties(FixtureDataMigration):
    fixture_specs = [
        ('intake', 'County', '0015_add_default_counties_data.json')
    ]

    @classmethod
    def forward(cls, *args):
        super().forward(*args)
        County = cls.get_model_class('intake', 'County', *args)
        FormSubmission = cls.get_model_class('intake', 'FormSubmission', *args)
        sf_county = County.filter(slug=Counties.SAN_FRANCISCO).first()
        for submission in FormSubmission.all():
            if submission.counties.count() < 1:
                submission.counties.add(sf_county)

    @classmethod
    def reverse(cls, *args):
        """just clears the 'county' m2m field on each submission
        """
        super().reverse(*args)


class Migration(migrations.Migration):

    dependencies = [
        ('intake', '0014_county_name'),
        ('user_accounts', '0006_add_county_model'),
    ]

    operations = [
        migrations.RunPython(
            AddDefaultCounties.forward,
            AddDefaultCounties.reverse)
    ]
