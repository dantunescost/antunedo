#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import connexion
from lib.mongoConnector import connect_to_mongodb, query_offers, geolocation_enumerations
from lib.utils import convert_geolocation_for_query, convert_params_to_price_filter, convert_params_to_surface_filter, \
                      convert_params_to_ground_surface_filter, convert_params_to_price_per_m2_filter, \
                      convert_params_to_price_per_are_filter, convert_params_to_magic_ratio_filter
from flask_cors import CORS


# Getting the best offers
def get_offers(geolocation=None, priceMin=0, priceMax=100000000, surfaceMin=0, surfaceMax=300, groundSurfaceMin=0,
               groundSurfaceMax=150, pricePerM2Min=0, pricePerM2Max=12000, pricePerAreMin=0, pricePerAreMax=1000000,
               magicRatioMin=-100, magicRatioMax=100, sort=None, sortOrder=None, nb_offers=200):
    client = connect_to_mongodb()

    geolocation = convert_geolocation_for_query(geolocation) if geolocation else {}
    price_filter = convert_params_to_price_filter(priceMin, priceMax)
    surface_filter = convert_params_to_surface_filter(surfaceMin, surfaceMax)
    ground_surface_filter = convert_params_to_ground_surface_filter(groundSurfaceMin, groundSurfaceMax)
    price_per_m2_filter = convert_params_to_price_per_m2_filter(pricePerM2Min, pricePerM2Max)
    price_per_are_filter = convert_params_to_price_per_are_filter(pricePerAreMin, pricePerAreMax)
    magic_ratio_filter = convert_params_to_magic_ratio_filter(magicRatioMin, magicRatioMax)
    result = query_offers(client, geolocation, price_filter, surface_filter, ground_surface_filter,
                          price_per_m2_filter, price_per_are_filter, magic_ratio_filter, sort, sortOrder, nb_offers)

    client.close()
    return result


# Function checking if user credentials are valid to connect to invest-af.com
def connect_admin(username, password):
    client = connect_to_mongodb()
    collection = client['antunedo']['admin_users']
    is_valid = collection.find_one({'username': username, 'password': password})
    client.close()
    return is_valid is not None


# Function returning every single possible geolocation
def geolocation_options():
    client = connect_to_mongodb()
    result = geolocation_enumerations(client)
    client.close()
    return result


########################################################################################################################


app = connexion.App(__name__, specification_dir='./specification/')
app.add_api('swagger.yaml')

if __name__ == "__main__":
    application = app.app
    CORS(app.app)
    app.run(port=8080, ssl_context='adhoc')
