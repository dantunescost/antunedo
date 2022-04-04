#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def convert_geolocation_for_query(geolocation):
    result = {}
    for i in geolocation:
        field = ('geo.' if i['type'] == 'country' or i['type'] == 'city' else 'completeGeoInfos.levels.') + i['type']
        if field in result:
            result[field]['$in'].append(i['name'])
        else:
            result[field] = {'$in': [i['name']]}
    return result


def convert_params_to_price_filter(price_min, price_max):
    if price_min == 0 and price_max == 100000000:
        return {}
    elif price_min == 0:
        return {'price': {'$lte': price_max}}
    elif price_max == 100000000:
        return {'price': {'$gte': price_min}}
    else:
        return {'price': {'$lte': price_max, '$gte': price_min}}


def convert_params_to_surface_filter(surface_min, surface_max):
    if surface_min == 0 and surface_max == 300:
        return {}
    elif surface_min == 0:
        return {'characteristic.property_surface': {'$lte': surface_max}}
    elif surface_max == 300:
        return {'characteristic.property_surface': {'$gte': surface_min}}
    else:
        return {'characteristic.property_surface': {'$lte': surface_max, '$gte': surface_min}}


def convert_params_to_ground_surface_filter(ground_surface_min, ground_surface_max):
    if ground_surface_min == 0 and ground_surface_max == 150:
        return {}
    elif ground_surface_min == 0:
        return {'characteristic.ground_surface': {'$lte': ground_surface_max}}
    elif ground_surface_max == 150:
        return {'characteristic.ground_surface': {'$gte': ground_surface_min}}
    else:
        return {'characteristic.ground_surface': {'$lte': ground_surface_max, '$gte': ground_surface_min}}


def convert_params_to_price_per_m2_filter(price_per_m2_min, price_per_m2_max):
    if price_per_m2_min == 0 and price_per_m2_max == 12000:
        return {}
    elif price_per_m2_min == 0:
        return {'price_by_m2': {'$lte': price_per_m2_max}}
    elif price_per_m2_max == 12000:
        return {'price_by_m2': {'$gte': price_per_m2_min}}
    else:
        return {'price_by_m2': {'$lte': price_per_m2_max, '$gte': price_per_m2_min}}


def convert_params_to_price_per_are_filter(price_per_are_min, price_per_are_max):
    if price_per_are_min == 0 and price_per_are_max == 1000000:
        return {}
    elif price_per_are_min == 0:
        return {'price_per_are': {'$lte': price_per_are_max}}
    elif price_per_are_max == 1000000:
        return {'price_per_are': {'$gte': price_per_are_min}}
    else:
        return {'price_per_are': {'$lte': price_per_are_max, '$gte': price_per_are_min}}


def convert_params_to_magic_ratio_filter(magic_ratio_min, magic_ratio_max):
    if magic_ratio_min == -100 and magic_ratio_max == 100:
        return {}
    elif magic_ratio_min == -100:
        return {'ratio_to_average_price': {'$lte': magic_ratio_max}}
    elif magic_ratio_max == 100:
        return {'ratio_to_average_price': {'$gte': magic_ratio_min}}
    else:
        return {'ratio_to_average_price': {'$lte': magic_ratio_max, '$gte': magic_ratio_min}}


def convert_params_to_property_types_filter(property_types):
    if not property_types:
        return {}
    else:
        return {'property.immotype.label': {'$in': property_types}}
