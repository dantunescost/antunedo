#!/usr/bin python3.7
# -*- coding: utf-8 -*-
import time

from lib.mongoConnector import connect_to_mongodb


def compute_average_prices():
    start = time.time()
    client = connect_to_mongodb()
    collection = client['antunedo']['offers']
    avg_collection = client['antunedo']['average_prices']

    # Get level 1 averages
    avg_prices = level_1_averages(collection)
    print("Level 1")
    for i in avg_prices:
        old_average = avg_collection.find_one({
            'immo_type_id': i['_id']['type_id'],
            'country': i['_id']['geo']['country'],
            'city': i['_id']['geo']['city'],
            'priority_level': 1
        })
        if old_average is None:
            avg_collection.insert_one({
                'immo_type_id': i['_id']['type_id'],
                'immo_type': i['_id']['type'],
                'country': i['_id']['geo']['country'],
                'city': i['_id']['geo']['city'],
                'priority_level': 1,
                'amount_of_properties': i['amount_of_properties'],
                'average_price': i['average']
            })
        else:
            if old_average['amount_of_properties'] != i['amount_of_properties'] \
                    or old_average['average_price'] != i['average']:
                avg_collection.update_one(
                    {
                        'immo_type_id': i['_id']['type_id'],
                        'country': i['_id']['geo']['country'],
                        'city': i['_id']['geo']['city'],
                        'priority_level': 1
                    },
                    {
                        '$set': {
                            'amount_of_properties': i['amount_of_properties'],
                            'average_price': i['average']
                        }
                    }
                )

    # Get level 2 averages
    avg_prices = level_2_averages(collection)
    print("Level 2")
    for i in avg_prices:
        old_average = avg_collection.find_one({
            'immo_type_id': i['_id']['type_id'],
            'country': i['_id']['geo']['country'],
            'city': i['_id']['geo']['city'],
            'bedrooms_count': i['_id']['bedrooms'],
            'priority_level': 2
        })
        if old_average is None:
            avg_collection.insert_one({
                'immo_type_id': i['_id']['type_id'],
                'immo_type': i['_id']['type'],
                'country': i['_id']['geo']['country'],
                'city': i['_id']['geo']['city'],
                'bedrooms_count': i['_id']['bedrooms'],
                'priority_level': 2,
                'amount_of_properties': i['amount_of_properties'],
                'average_price': i['average']
            })
        else:
            if old_average['amount_of_properties'] != i['amount_of_properties'] \
                    or old_average['average_price'] != i['average']:
                avg_collection.update_one(
                    {
                        'immo_type_id': i['_id']['type_id'],
                        'country': i['_id']['geo']['country'],
                        'city': i['_id']['geo']['city'],
                        'bedrooms_count': i['_id']['bedrooms'],
                        'priority_level': 2
                    },
                    {
                        '$set': {
                            'amount_of_properties': i['amount_of_properties'],
                            'average_price': i['average']
                        }
                    }
                )

    # Get level 3 averages
    avg_prices = level_3_averages(collection)
    print("Level 3")
    for i in avg_prices:
        old_average = avg_collection.find_one({
            'immo_type_id': i['_id']['type_id'],
            'country': i['_id']['geo']['country'],
            'city': i['_id']['geo']['city'],
            'city_district': i['_id']['city_district'],
            'priority_level': 3
        })
        if old_average is None:
            avg_collection.insert_one({
                'immo_type_id': i['_id']['type_id'],
                'immo_type': i['_id']['type'],
                'country': i['_id']['geo']['country'],
                'city': i['_id']['geo']['city'],
                'city_district': i['_id']['city_district'],
                'priority_level': 3,
                'amount_of_properties': i['amount_of_properties'],
                'average_price': i['average']
            })
        else:
            if old_average['amount_of_properties'] != i['amount_of_properties'] \
                    or old_average['average_price'] != i['average']:
                avg_collection.update_one(
                    {
                        'immo_type_id': i['_id']['type_id'],
                        'country': i['_id']['geo']['country'],
                        'city': i['_id']['geo']['city'],
                        'city_district': i['_id']['city_district'],
                        'priority_level': 3
                    },
                    {
                        '$set': {
                            'amount_of_properties': i['amount_of_properties'],
                            'average_price': i['average']
                        }
                    }
                )

    # Get level 4 averages
    avg_prices = level_4_averages(collection)
    print("Level 4")
    for i in avg_prices:
        old_average = avg_collection.find_one({
            'immo_type_id': i['_id']['type_id'],
            'country': i['_id']['geo']['country'],
            'city': i['_id']['geo']['city'],
            'city_district': i['_id']['city_district'],
            'bedrooms_count': i['_id']['bedrooms'],
            'priority_level': 4
        })
        if old_average is None:
            avg_collection.insert_one({
                'immo_type_id': i['_id']['type_id'],
                'immo_type': i['_id']['type'],
                'country': i['_id']['geo']['country'],
                'city': i['_id']['geo']['city'],
                'city_district': i['_id']['city_district'],
                'bedrooms_count': i['_id']['bedrooms'],
                'priority_level': 4,
                'amount_of_properties': i['amount_of_properties'],
                'average_price': i['average']
            })
        else:
            if old_average['amount_of_properties'] != i['amount_of_properties'] \
                    or old_average['average_price'] != i['average']:
                avg_collection.update_one(
                    {
                        'immo_type_id': i['_id']['type_id'],
                        'country': i['_id']['geo']['country'],
                        'city': i['_id']['geo']['city'],
                        'city_district': i['_id']['city_district'],
                        'bedrooms_count': i['_id']['bedrooms'],
                        'priority_level': 4
                    },
                    {
                        '$set': {
                            'amount_of_properties': i['amount_of_properties'],
                            'average_price': i['average']
                        }
                    }
                )

    print("\nComputing of average prices took {0:.2f}".format(time.time() - start) + " secs\n")
    client.close()


def level_1_averages(offres_collection):
    avg_prices = offres_collection.aggregate([
        {
            '$match': {
                'insertion_time': {'$gt': int(time.time()) - 86400 * 30 * 6},
                'price_by_m2': {'$exists': True, '$gte': 100, '$lt': 30000}
            }
        },
        {
            '$project': {
                'property.immotype.label': 1,
                'property.immotype.id': 1,
                'geo': 1,
                'price_by_m2': 1
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
    return avg_prices


def level_2_averages(offres_collection):
    avg_prices = offres_collection.aggregate([
        {
            '$match': {
                'insertion_time': {'$gt': int(time.time()) - 86400 * 30 * 6},
                'price_by_m2': {'$exists': True, '$gte': 100, '$lt': 30000},
                'characteristic.bedrooms_count': {'$gt': 0}
            }
        },
        {
            '$project': {
                'property.immotype.label': 1,
                'property.immotype.id': 1,
                'geo': 1,
                'price_by_m2': 1,
                'characteristic.bedrooms_count': 1
            }
        },
        {
            '$group': {
                '_id': {
                    'type': '$property.immotype.label',
                    'type_id': '$property.immotype.id',
                    'bedrooms': '$characteristic.bedrooms_count',
                    'geo': '$geo'
                },
                'amount_of_properties': {'$sum': 1},
                'average': {'$avg': '$price_by_m2'}
            }
        },
        {
            '$match': {
                'amount_of_properties': {'$gt': 3}
            }
        }
    ])
    return avg_prices


def level_3_averages(offres_collection):
    avg_prices_1 = offres_collection.aggregate([
        {
            '$match': {
                'insertion_time': {'$gt': int(time.time()) - 86400 * 30 * 6},
                'price_by_m2': {'$exists': True, '$gte': 100, '$lt': 30000},
                'completeGeoInfos.levels.L10': {'$exists': True}
            }
        },
        {
            '$project': {
                'property.immotype.label': 1,
                'property.immotype.id': 1,
                'geo': 1,
                'price_by_m2': 1,
                'completeGeoInfos.levels.L10': 1
            }
        },
        {
            '$group': {
                '_id': {
                    'type': '$property.immotype.label',
                    'type_id': '$property.immotype.id',
                    'city_district': '$completeGeoInfos.levels.L10',
                    'geo': '$geo'
                },
                'amount_of_properties': {'$sum': 1},
                'average': {'$avg': '$price_by_m2'}
            }
        },
        {
            '$match': {
                'amount_of_properties': {'$gt': 3}
            }
        }
    ])
    avg_prices_2 = offres_collection.aggregate([
        {
            '$match': {
                'insertion_time': {'$gt': int(time.time()) - 86400 * 30 * 6},
                'price_by_m2': {'$exists': True, '$gte': 100, '$lt': 30000},
                'completeGeoInfos.levels.L10': {'$exists': False},
                'completeGeoInfos.levels.L9': {'$exists': True}
            }
        },
        {
            '$project': {
                'property.immotype.label': 1,
                'property.immotype.id': 1,
                'geo': 1,
                'price_by_m2': 1,
                'completeGeoInfos.levels.L9': 1
            }
        },
        {
            '$group': {
                '_id': {
                    'type': '$property.immotype.label',
                    'type_id': '$property.immotype.id',
                    'city_district': '$completeGeoInfos.levels.L9',
                    'geo': '$geo'
                },
                'amount_of_properties': {'$sum': 1},
                'average': {'$avg': '$price_by_m2'}
            }
        },
        {
            '$match': {
                'amount_of_properties': {'$gt': 3}
            }
        }
    ])
    return list(avg_prices_1) + list(avg_prices_2)


def level_4_averages(offres_collection):
    avg_prices_1 = offres_collection.aggregate([
        {
            '$match': {
                'insertion_time': {'$gt': int(time.time()) - 86400 * 30 * 6},
                'price_by_m2': {'$exists': True, '$gte': 100, '$lt': 30000},
                'completeGeoInfos.levels.L10': {'$exists': True},
                'characteristic.bedrooms_count': {'$gt': 0}
            }
        },
        {
            '$project': {
                'property.immotype.label': 1,
                'property.immotype.id': 1,
                'geo': 1,
                'price_by_m2': 1,
                'characteristic.bedrooms_count': 1,
                'completeGeoInfos.levels.L10': 1
            }
        },
        {
            '$group': {
                '_id': {
                    'type': '$property.immotype.label',
                    'type_id': '$property.immotype.id',
                    'bedrooms': '$characteristic.bedrooms_count',
                    'city_district': '$completeGeoInfos.levels.L10',
                    'geo': '$geo'
                },
                'amount_of_properties': {'$sum': 1},
                'average': {'$avg': '$price_by_m2'}
            }
        },
        {
            '$match': {
                'amount_of_properties': {'$gt': 3}
            }
        }
    ])
    avg_prices_2 = offres_collection.aggregate([
        {
            '$match': {
                'insertion_time': {'$gt': int(time.time()) - 86400 * 30 * 6},
                'price_by_m2': {'$exists': True, '$gte': 100, '$lt': 30000},
                'completeGeoInfos.levels.L10': {'$exists': False},
                'completeGeoInfos.levels.L9': {'$exists': True},
                'characteristic.bedrooms_count': {'$gt': 0}
            }
        },
        {
            '$project': {
                'property.immotype.label': 1,
                'property.immotype.id': 1,
                'geo': 1,
                'price_by_m2': 1,
                'completeGeoInfos.levels.L9': 1,
                'characteristic.bedrooms_count': 1
            }
        },
        {
            '$group': {
                '_id': {
                    'type': '$property.immotype.label',
                    'type_id': '$property.immotype.id',
                    'city_district': '$completeGeoInfos.levels.L9',
                    'bedrooms': '$characteristic.bedrooms_count',
                    'geo': '$geo'
                },
                'amount_of_properties': {'$sum': 1},
                'average': {'$avg': '$price_by_m2'}
            }
        },
        {
            '$match': {
                'amount_of_properties': {'$gt': 3}
            }
        }
    ])
    return list(avg_prices_1) + list(avg_prices_2)


if __name__ == "__main__":
    compute_average_prices()
