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


def pop_offers_already_saved(client, offers):
    ids = []
    collection = client['antunedo']['raw_data']
    for i in offers:
        ids.append(i["id"])
    res = collection.aggregate([
        {
            '$match': {
                'id': {'$in': ids}
            }
        },
        {
            '$project': {
                'id': 1
            }
        },
        {
            '$group': {
                '_id': None,
                'ids': {'$push': '$id'}
            }
        }
    ])
    ids_to_pop = []
    for i in res:
        ids_to_pop = i['ids']
    return ids_to_pop


def get_last_maradona_execution(client):
    collection = client['antunedo']['logs']
    result = 1564358400
    res = collection.aggregate([
        {
            '$sort': {
                'start_time': -1
            }
        },
        {
            '$limit': 1
        }
    ])
    for i in res:
        result = i['start_time']
    return result
