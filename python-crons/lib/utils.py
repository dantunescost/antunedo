#!/usr/bin python3.7
# -*- coding: utf-8 -*-
from datetime import datetime
import pytz

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
            and 'price' in offer \
            and offer['property']['characteristic']['property_surface'] > 10 \
            and offer['price'] > 10000:
        offer['price_by_m2'] = offer['price'] / offer['property']['characteristic']['property_surface']
        # Check if fields exist and get average price for similar goods and compute ratio to average price
        if 'property' in offer and 'immotype' in offer['property'] and 'id' in offer['property']['immotype'] \
                and 'geo' in offer and 'city' in offer['geo']:
            average_price = avg_collection.find_one({
                'immo_type_id': offer['property']['immotype']['id'],
                'city': offer['geo']['city']
            })
            if average_price is not None:
                offer['ratio_to_average_price'] = round(
                    ((offer['price_by_m2'] / average_price['average_price']) - 1) * 100,
                    3
                )
                offer['properties_used_to_calculate_average'] = average_price['amount_of_properties']
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
                            send_slack_alert(alert_channel, title, url, price, surface, offer['price_by_m2'],
                                             offer['id'], offer['properties_used_to_calculate_average'],
                                             offer['ratio_to_average_price'], photo_url)
                    elif offer['ratio_to_average_price'] < -25:
                        send_slack_alert("alertes_etranger", title, url, price, surface, offer['price_by_m2'],
                                         offer['id'], offer['properties_used_to_calculate_average'],
                                         offer['ratio_to_average_price'], photo_url)
