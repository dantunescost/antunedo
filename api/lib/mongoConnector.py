#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import configparser
import os

from pymongo import MongoClient, DESCENDING, ASCENDING

path = os.path.dirname(os.path.abspath(__file__))
config = configparser.ConfigParser()
config.read(path + '''/../config/configuration.cfg''')


def connect_to_mongodb():
    client = MongoClient(
        'mongodb://' + config['MONGODB']['User'] + ':' + config['MONGODB']['Password'] + '@' + config['MONGODB'][
            'Host'] + ':' + config['MONGODB']['Port'] + '/admin')
    return client


def query_offers(client, geolocation, price_filter, surface_filter, ground_surface_filter, price_per_m2_filter,
                 price_per_are_filter, magic_ratio_filter, sort, sort_order, limit_offers):
    collection = client['antunedo']['offers']
    field_to_sort_by, direction = convert_sort_instructions(sort, sort_order)
    results = []
    query = collection.find({**{'ratio_to_average_price': {'$lt': -14.9}, 'geo.country': 'lu'},
                             **geolocation,
                             **price_filter,
                             **surface_filter,
                             **ground_surface_filter,
                             **price_per_m2_filter,
                             **price_per_are_filter,
                             **magic_ratio_filter}) \
                .sort([(field_to_sort_by, direction)]) \
                .limit(limit_offers)
    print({**{'ratio_to_average_price': {'$lt': -14.9}, 'geo.country': 'lu'},
                             **geolocation,
                             **price_filter,
                             **surface_filter,
                             **ground_surface_filter,
                             **price_per_m2_filter,
                             **price_per_are_filter,
                             **magic_ratio_filter})
    for i in query:
        try:
            insertion_date = int(i['insertion_time'])
        except KeyError:
            insertion_date = -1
        try:
            url = "https://athome.lu" + i['meta']['permalink']['fr']
        except KeyError:
            url = "https://athome.lu"
        try:
            immo_type = i['immotype']
        except KeyError:
            immo_type = "Bien inconnu"
        try:
            bedrooms = i['characteristic']['bedrooms_count']
        except KeyError:
            bedrooms = 0
        try:
            city = i['geo']['city']
        except KeyError:
            city = ""
        try:
            surface = i['characteristic']['property_surface']
        except KeyError:
            surface = 0
        title = immo_type + " " + str(bedrooms) + " chambres à " + city
        try:
            region = i['completeGeoInfos']['levels']['L4']
        except KeyError:
            region = ""
        try:
            price = i['price']
        except KeyError:
            price = 0
        if price != 0 and surface != 0:
            price_per_m2 = price / surface
        else:
            price_per_m2 = 0
        try:
            energy_pass = i['property']['energy_efficiency']['lu_energy_class']
        except KeyError:
            energy_pass = ""
        try:
            magic_ratio = i['ratio_to_average_price']
        except KeyError:
            magic_ratio = 0
        try:
            switcher = {
                1: "(simple)",
                2: "(ch)",
                3: "(quartier)",
                4: "(ch + quartier)"
            }
            pertinence = str(int(i['properties_used_to_calculate_average'])) + " biens " \
                               + switcher[int(i['average_price_pertinence_level'])]
        except KeyError:
            pertinence = ""
        try:
            latitude = i['completeGeoInfos']['pin']['lat']
            longitude = i['completeGeoInfos']['pin']['lon']
            maps_link = "https://www.google.com/maps/search/?api=1&query=" + str(latitude) + "," \
                        + str(longitude)
        except KeyError:
            maps_link = None
        try:
            ground_surface = i['characteristic']['ground_surface']
        except KeyError:
            ground_surface = 0
        if price != 0 and ground_surface != 0:
            price_per_are = price / ground_surface
        else:
            price_per_are = 0
        results.append({
            "id": i['id'],
            "insertion_date": insertion_date,
            "title": title,
            "url": url,
            "surface": surface,
            "city": city,
            "region": region,
            "bedrooms": bedrooms,
            "price": price,
            "price_per_m2": price_per_m2,
            "energy_pass": energy_pass,
            "magic_ratio": magic_ratio,
            "maps_link": maps_link,
            "pertinence": pertinence,
            "ground_surface": ground_surface,
            "price_per_are": price_per_are
        })
    return results


def convert_sort_instructions(sort, sort_order):
    if sort is None:
        return 'insertion_time', DESCENDING
    else:
        switcher = {
            'date': 'insertion_time',
            'city': 'geo.city',
            'price': 'price',
            'surface': 'characteristic.property_surface',
            'prixPerM2': 'price_by_m2',
            'groundSurface': 'characteristic.ground_surface',
            'prixPerAre': 'price_per_are',
            'ratio': 'ratio_to_average_price'
        }
        field = switcher.get(sort, 'insertion_time')
        return field, DESCENDING if sort_order == 'desc' else ASCENDING


def geolocation_enumerations(client):
    collection = client['antunedo']['geographical_filter_options']
    result = []
    for i in collection.find({}):
        result += i['options']
    return result


def geolocation_enumerations_obsolete(client):
    collection = client['antunedo']['offers']
    cities = []
    iterator = collection.aggregate([
        {
            '$group': {
                '_id': {
                    'type': 'city',
                    'name': '$geo.city',
                    'country': '$geo.country'
                }
            }
        },
        {
            '$sort': {
                '_id.name': 1
            }
        },
        {
            '$group': {
                '_id': None,
                'cities': {'$push': '$_id'}
            }
        },
    ])
    for i in iterator:
        cities = i['cities']
        break
    countries = []
    iterator = collection.aggregate([
        {
            '$group': {
                '_id': {
                    'type': 'country',
                    'name': '$geo.country',
                    'country': '$geo.country'
                }
            }
        },
        {
            '$sort': {
                '_id.name': 1
            }
        },
        {
            '$group': {
                '_id': None,
                'countries': {'$push': '$_id'}
            }
        },
    ])
    for i in iterator:
        countries = i['countries']
        break
    regions_and_other = []
    iterator = collection.aggregate([
        {
            '$project': {
                'pays': '$geo.country',
                'completeGeoInfos.levels.L4': 1,
                'completeGeoInfos.levels.L5': 1,
                'completeGeoInfos.levels.L7': 1,
                'completeGeoInfos.levels.L10': 1,
            }
        },
        {
            '$project': {
                'pays': 1,
                'levels': {'$objectToArray': '$completeGeoInfos.levels'}
            }
        },
        {
            '$unwind': '$levels'
        },
        {
            '$group': {
                '_id': {
                    'type': '$levels.k',
                    'length': {'$strLenCP': '$levels.k'},
                    'name': '$levels.v',
                    'country': '$pays'
                }
            }
        },
        {
            '$sort': {
                '_id.length': 1,
                '_id.type': 1,
                '_id.name': 1
            }
        },
        {
            '$project': {
                '_id.type': 1,
                '_id.name': 1,
                '_id.country': 1
            }
        },
        {
            '$group': {
                '_id': None,
                'regions_and_other': {'$push': '$_id'}
            }
        }
    ])
    for i in iterator:
        regions_and_other = i['regions_and_other']
        break
    return countries + cities[3:] + regions_and_other
