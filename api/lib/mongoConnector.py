#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import configparser
import os

from pymongo import MongoClient

path = os.path.dirname(os.path.abspath(__file__))
config = configparser.ConfigParser()
config.read(path + '''/../config/configuration.cfg''')


def connect_to_mongodb():
    client = MongoClient(
        'mongodb://' + config['MONGODB']['User'] + ':' + config['MONGODB']['Password'] + '@' + config['MONGODB'][
            'Host'] + ':' + config['MONGODB']['Port'] + '/admin')
    return client


def query_offers(client, limit_offers):
    collection = client['antunedo']['raw_data']
    results = []
    query = collection.find({}).limit(limit_offers)
    for i in query:
        try:
            url = "athome.lu" + i['meta']['permalink']['fr']
        except KeyError:
            url = "athome.lu"
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
        results.append({
            "title": title,
            "url": url,
            "surface": surface,
            "city": city,
            "region": region,
            "bedrooms": bedrooms,
            "price": price,
            "price_per_m2": price_per_m2,
            "energy_pass": energy_pass
        })
    return results
