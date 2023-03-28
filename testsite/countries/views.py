from django.http import JsonResponse
import json
from .models import Country, Region
from functools import reduce


def init_regions(region):
		return {
				'name': region['name'],
				'id': region['id'],
				'number_countries': 0,
				'total_population': 0
		}

def stats(request):
		countries = list(Country.objects.values())
		regions = list(Region.objects.values())
		org_list = list(map(init_regions, regions))
		for cou in countries:
				for reg in org_list:
						if cou['region_id'] == reg['id']:
								reg['number_countries'] += 1
								reg['total_population'] += cou['population']
		for reg in org_list:
			reg.pop('id', None)

		response = {"regions": org_list}
		return JsonResponse(response)
