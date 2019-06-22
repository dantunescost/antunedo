#!/usr/bin python3.7
# -*- coding: utf-8 -*-

from lib.mongoConnector import connect_to_mongodb
from lib.queryBuilder import query_immo_offers, get_amount_of_pages


if __name__ == "__main__":
    client = connect_to_mongodb()
    db = client['antunedo']
    collection = db['raw_data']

    print('starting ...')
    total_pages = get_amount_of_pages()
    for i in range(total_pages):
        result = query_immo_offers(i)
        print("Processing data... " + "{0:.2f}".format((i / total_pages) * 100) + "%", end='\r')
        for offer in result:
            collection.update_one({"id": offer["id"]}, {"$set": offer}, upsert=True)
        i += 1

    client.close()
