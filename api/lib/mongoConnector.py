#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import configparser
import os

from pymongo import MongoClient, DESCENDING

path = os.path.dirname(os.path.abspath(__file__))
config = configparser.ConfigParser()
config.read(path + '''/../config/configuration.cfg''')


def connect_to_mongodb():
    client = MongoClient(
        'mongodb://' + config['MONGODB']['User'] + ':' + config['MONGODB']['Password'] + '@' + config['MONGODB'][
            'Host'] + ':' + config['MONGODB']['Port'] + '/admin')
    return client


def query_offers(client, country, limit_offers):
    collection = client['antunedo']['offers']
    results = []
    if country is not None:
        query = collection.find({'ratio_to_average_price': {'$lt': -14.9}, 'geo.country': {'$in': country}})\
                    .sort([("insertion_time", DESCENDING)]) \
                    .limit(limit_offers)
    else:
        query = collection.find({'ratio_to_average_price': {'$lt': -14.9}, 'geo.country': 'lu'}) \
            .sort([("insertion_time", DESCENDING)]) \
            .limit(limit_offers)

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
