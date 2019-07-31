#!/usr/bin python3.7
# -*- coding: utf-8 -*-
from datetime import datetime


def get_time_string(timestamp):
    date_obj = datetime.fromtimestamp(timestamp)
    return date_obj.strftime("%Y%m%dT%H%M%SZ")


def add_fields_to_offer(offer, timestamp, avg_collection):
    offer['insertion_time'] = timestamp
    if 'property' in offer and 'characteristic' in offer['property'] \
            and 'property_surface' in offer['property']['characteristic'] \
            and 'price' in offer \
            and offer['property']['characteristic']['property_surface'] > 10 \
            and offer['price'] > 10000:
        offer['price_by_m2'] = offer['price'] / offer['property']['characteristic']['property_surface']
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
