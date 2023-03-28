import json
import os
import requests

from django.conf import settings
from django.core.management.base import BaseCommand

from countries.models import Country, Region, TopLevelDomain


class Command(BaseCommand):
    help = "Loads country data from a JSON file."

    IMPORT_FILE = os.path.join(
        settings.BASE_DIR, "..", "data", "countries.json")

    def get_data(self):
        # with open(self.IMPORT_FILE) as f:
        #     data = json.load(f)
        resp = requests.get(
            'https://storage.googleapis.com/dcr-django-test/countries.json')
        return resp.json()

    def handle(self, *args, **options):
        data = self.get_data()
        for row in data:
            tld_list = []
            for tld_str in row['topLevelDomain']:
                tld, tld_created = TopLevelDomain.objects.get_or_create(
                    tld=tld_str)
                if tld_created:
                    self.stdout.write(
                        self.style.SUCCESS("TLD: {} - Created".format(tld))
                )
                tld_list.append(tld)
            region, region_created = Region.objects.get_or_create(
                name=row["region"])
            if region_created:
                self.stdout.write(
                    self.style.SUCCESS("Region: {} - Created".format(region))
                )
            country, country_created = Country.objects.get_or_create(
                name=row["name"],
                defaults={
                    "alpha2Code": row["alpha2Code"],
                    "alpha3Code": row["alpha3Code"],
                    "population": row["population"],
                    "capital": row["capital"],
                    "region": region,
                    # "topLevelDomain": []
                },
            )
            country.topLevelDomain.set(tld_list)

            self.stdout.write(
                self.style.SUCCESS(
                    "{} - {}".format(
                        country, "Created" if country_created else "Updated"
                    )
                )
            )
