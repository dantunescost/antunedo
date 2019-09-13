#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import connexion
from lib.mongoConnector import connect_to_mongodb, query_offers
from flask_cors import CORS


def get_offers(city=None, nb_offers=20):
    client = connect_to_mongodb()
    if city is not None:
        print('Filter by city')

    result = query_offers(client, nb_offers)

    client.close()
    return result

########################################################################################################################


app = connexion.App(__name__, specification_dir='./specification/')
app.add_api('swagger.yaml')

if __name__ == "__main__":
    application = app.app
    # CORS_RESOURCES = {r"/v1/*": {"origins": "*"}, r"/v1.0/*": {"origins": "*"}, r"/v1.1/*": {"origins": "*"}}
    CORS(app.app)
    app.run(port=8080)
