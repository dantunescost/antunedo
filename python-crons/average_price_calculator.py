#!/usr/bin python3.7
# -*- coding: utf-8 -*-
import time

from lib.mongoConnector import connect_to_mongodb


def main():
    start = time.time()
    client = connect_to_mongodb()
    collection = client['antunedo']['offers']

    res = collection.find(
        {
            'property.characteristic.property_surface': {'$exists': True, '$gt': 10},
            'price': {'$exists': True, '$gt': 10000}
        },
        {
            'property.characteristic.property_surface': 1,
            'id': 1,
            'price': 1
        }
    )

    cpt = 0
    for i in res:
        if cpt % 50 == 0:
            print("Processing tracking data... " + "{0:.2f}".format((cpt / 26849) * 100) + "% in "
                  + "{0:.2f}".format(time.time() - start) + " secs", end='\r')
        price_by_m2 = i['price'] / i['property']['characteristic']['property_surface']
        collection.update_one({'id': i['id']}, {'$set': {'price_by_m2': price_by_m2}})
        cpt += 1

    client.close()


def compute_average_prices():
    start = time.time()
    client = connect_to_mongodb()
    collection = client['antunedo']['offers']
    avg_collection = client['antunedo']['average_prices']

    avg_prices = collection.aggregate([
        {
            '$project': {
                'property.immotype.label': 1,
                'property.immotype.id': 1,
                'geo': 1,
                'price_by_m2': 1
            }
        },
        {
            '$match': {
                'price_by_m2': {'$exists': True}
            }
        },
        {
            '$group': {
                '_id': {
                    'type': '$property.immotype.label',
                    'type_id': '$property.immotype.id',
                    'geo': '$geo'
                },
                'amount_of_properties': {'$sum': 1},
                'average': {'$avg': '$price_by_m2'}
            }
        }
    ])
    for i in avg_prices:
        avg_collection.replace_one(
            {
                'immo_type_id': i['_id']['type_id'],
                'city': i['_id']['geo']['city']
            },
            {
                'immo_type_id': i['_id']['type_id'],
                'immo_type': i['_id']['type'],
                'country': i['_id']['geo']['country'],
                'city': i['_id']['geo']['city'],
                'amount_of_properties': i['amount_of_properties'],
                'average_price': i['average']
            },
            upsert=True
        )

    print("\nComputing of average prices took {0:.2f}".format(time.time() - start) + " secs\n")
    client.close()


def compute_ratio_to_average_price():
    start = time.time()
    client = connect_to_mongodb()
    collection = client['antunedo']['offers']
    avg_collection = client['antunedo']['average_prices']
    average_prices_dict = {}
    print("Storing average prices ... \n")
    for i in avg_collection.find():
        average_prices_dict[str(i['immo_type_id']) + str(i['city'])] = i['average_price']

    offers_cursor = collection.find({'ratio_to_average_price': {'$exists': False}})
    cpt = 0
    for offer in offers_cursor:
        if cpt % 100 == 0:
            print(cpt)
        cpt += 1
        if 'price_by_m2' in offer and 'property' in offer and 'immotype' in offer['property'] \
                and 'id' in offer['property']['immotype'] \
                and 'geo' in offer and 'city' in offer['geo']:
            average_price = None if (str(offer['property']['immotype']['id']) + str(
                offer['geo']['city'])) not in average_prices_dict else average_prices_dict[
                str(offer['property']['immotype']['id']) + str(offer['geo']['city'])]
            if average_price is not None:
                magic_ratio = round(((offer['price_by_m2'] / average_price) - 1) * 100, 3)
                collection.update_one({'id': offer['id']}, {'$set': {'ratio_to_average_price': magic_ratio}})

    print("\nComputing took {0:.2f}".format(time.time() - start) + " secs\n")
    client.close()


if __name__ == "__main__":
    compute_average_prices()
