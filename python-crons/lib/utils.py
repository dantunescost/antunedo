#!/usr/bin python3.7
# -*- coding: utf-8 -*-
import time
from datetime import datetime
import pytz

from lib.mongoConnector import connect_to_mongodb
from lib.slack_alerts import send_slack_alert


def get_time_string(timestamp):
    tz = pytz.timezone('Europe/Luxembourg')
    date_obj = datetime.fromtimestamp(timestamp, tz)
    return date_obj.strftime("%Y%m%dT%H%M%SZ")


def add_fields_to_offer(offer, timestamp, avg_collection):
    offer['insertion_time'] = timestamp
    # Check if fields exist and compute price per square meter
    if 'property' in offer and 'characteristic' in offer['property'] \
            and 'property_surface' in offer['property']['characteristic'] \
            and 'price' in offer and 10 < offer['property']['characteristic']['property_surface'] < 1000000 \
            and 10000 < offer['price'] < 100000000:
        offer['price_by_m2'] = offer['price'] / offer['property']['characteristic']['property_surface']
        # Check if fields exist and get average price for similar goods and compute ratio to average price
        if 'property' in offer and 'immotype' in offer['property'] and 'id' in offer['property']['immotype'] \
                and 'geo' in offer and 'city' in offer['geo']:
            # Getting best possible average
            average_price = None
            avg_price_aggregator = [
                {
                    '$match': {
                        'immo_type_id': offer['property']['immotype']['id'],
                        'country': offer['geo']['country'],
                        'city': offer['geo']['city']
                    }
                },
                {
                    '$sort': {
                        'priority_level': -1
                    }
                }
            ]
            if 'completeGeoInfos' in offer and 'levels' in offer['completeGeoInfos']:
                if 'L10' in offer['completeGeoInfos']['levels']:
                    avg_price_aggregator[0]['$match']['city_district'] = {
                        '$in': [offer['completeGeoInfos']['levels']['L10'], None]
                    }
                elif 'L9' in offer['completeGeoInfos']['levels']:
                    avg_price_aggregator[0]['$match']['city_district'] = {
                        '$in': [offer['completeGeoInfos']['levels']['L9'], None]
                    }
            if 'characteristic' in offer and 'bedrooms_count' in offer['characteristic']:
                avg_price_aggregator[0]['$match']['bedrooms_count'] = {
                    '$in': [offer['characteristic']['bedrooms_count'], None]
                }
            if 'characteristic' in offer and 'ground_surface' in offer['characteristic'] and \
                    offer['characteristic']['ground_surface'] != 0:
                offer['price_per_are'] = offer['price'] / offer['characteristic']['ground_surface']
                avg_price_aggregator[0]['$match']['bedrooms_count'] = {
                    '$in': [offer['characteristic']['bedrooms_count'], None]
                }
            avg_price_cursor = avg_collection.aggregate(avg_price_aggregator)
            for i in avg_price_cursor:
                average_price = i
                break
            if average_price is not None:
                offer['ratio_to_average_price'] = round(
                    ((offer['price_by_m2'] / average_price['average_price']) - 1) * 100,
                    3
                )
                offer['properties_used_to_calculate_average'] = average_price['amount_of_properties']
                offer['average_price_pertinence_level'] = average_price['priority_level']
                # Send Slack alerts
                if offer['properties_used_to_calculate_average'] >= 5:
                    city = ""
                    try:
                        url = "https://athome.lu" + offer['meta']['permalink']['fr']
                    except KeyError:
                        url = ""
                    try:
                        immo_type = offer['immotype']
                    except KeyError:
                        immo_type = "Bien inconnu"
                    try:
                        bedrooms = offer['characteristic']['bedrooms_count']
                    except KeyError:
                        bedrooms = 0
                    try:
                        city = offer['geo']['city']
                        if city == "Luxembourg":
                            city += "-" + offer['completeGeoInfos']['levels']['L10']
                    except KeyError:
                        if not city:
                            city = " ville inconnue"
                    try:
                        photo_url = offer['config']['urlPicture'] + offer['config']['layout']['path_picture'] \
                                    + offer['media']['items'][0]['uri']
                    except (KeyError, IndexError):
                        photo_url = ""
                    try:
                        surface = offer['characteristic']['property_surface']
                    except KeyError:
                        surface = 0
                    try:
                        latitude = offer['completeGeoInfos']['pin']['lat']
                        longitude = offer['completeGeoInfos']['pin']['lon']
                        maps_link = "https://www.google.com/maps/search/?api=1&query=" + str(latitude) + "," \
                                    + str(longitude)
                    except KeyError:
                        maps_link = None
                    try:
                        country = offer['geo']['country']
                        if 'completeGeoInfos' in offer and 'levels' in offer['completeGeoInfos'] and \
                                'L2' in offer['completeGeoInfos']['levels']:
                            country = offer['completeGeoInfos']['levels']['L2']
                    except KeyError:
                        country = ""
                    title = immo_type + " " + str(bedrooms) + " bedrooms in " + city
                    if country not in ["lu", "Luxembourg"]:
                        title += ", " + country
                    try:
                        price = offer['price']
                    except KeyError:
                        price = 0
                    alert_channel = ""
                    if offer['geo']['country'] == "lu":
                        if offer['ratio_to_average_price'] < -50:
                            alert_channel = "#alertes_niv_1"
                        elif offer['ratio_to_average_price'] < -25:
                            alert_channel = "#alertes_niv_2"
                        elif offer['ratio_to_average_price'] < -15:
                            alert_channel = "#alertes_niv_3"
                        if offer['ratio_to_average_price'] < -15:
                            print("\nALERT !\n")
                            send_slack_alert(alert_channel, title, url, price, surface, offer['price_by_m2'],
                                             offer['id'], offer['properties_used_to_calculate_average'],
                                             average_price['priority_level'], offer['ratio_to_average_price'],
                                             photo_url, maps_link)
                    elif offer['ratio_to_average_price'] < -25:
                        send_slack_alert("alertes_etranger", title, url, price, surface, offer['price_by_m2'],
                                         offer['id'], offer['properties_used_to_calculate_average'],
                                         average_price['priority_level'], offer['ratio_to_average_price'],
                                         photo_url, maps_link)
                        print("\nALERT !\n")


def compute_price_per_are_meter_for_all():
    start = time.time()
    client = connect_to_mongodb()
    collection = client['antunedo']['offers']

    res = collection.find(
        {
            'characteristic.ground_surface': {'$exists': True, '$gt': 0},
            'price': {'$exists': True, '$gt': 10000},
            'price_per_are': {'$exists': False}
        },
        {
            'characteristic.ground_surface': 1,
            'id': 1,
            'price': 1
        }
    )

    cpt = 0
    for i in res:
        if cpt % 50 == 0:
            print("Processing tracking data... " + "{0:.2f}".format((cpt / 37958) * 100) + "% in "
                  + "{0:.2f}".format(time.time() - start) + " secs", end='\r')
        price_by_m2 = i['price'] / i['characteristic']['ground_surface']
        collection.update_one({'id': i['id']}, {'$set': {'price_per_are': price_by_m2}})
        cpt += 1

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


def compute_properties_used_to_calculate_average():
    start = time.time()
    client = connect_to_mongodb()
    collection = client['antunedo']['offers']
    avg_collection = client['antunedo']['average_prices']
    cpt = 0
    avg_prices = avg_collection.find()
    for i in avg_prices:
        print(cpt)
        cpt += 1
        collection.update_many(
            {
                'ratio_to_average_price': {'$exists': True},
                'properties_used_to_calculate_average': {'$exists': False},
                'property.immotype.id': i['immo_type_id'],
                'geo.city': i['city']
            },
            {
                '$set': {
                    'properties_used_to_calculate_average': i['amount_of_properties']
                }
            }
        )

    print("\nComputing of average prices took {0:.2f}".format(time.time() - start) + " secs\n")
    client.close()


if __name__ == "__main__":
    compute_price_per_are_meter_for_all()
