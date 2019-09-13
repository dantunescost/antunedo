#!/usr/bin python3.7
# -*- coding: utf-8 -*-
from pymongo.errors import DuplicateKeyError

from lib.mongoConnector import connect_to_mongodb, pop_offers_already_saved
from lib.queryBuilder import query_immo_offers, get_amount_of_pages


def get_offers_by_immotype(collection, immotype, total_pages, sort="asc"):
    if total_pages == 0:
        return
    i = 0
    while i <= total_pages and i <= 500:
        result = query_immo_offers(i, immotype, sort)
        print("Processing data... " + "{0:.2f}".format((i / total_pages) * 100) + "%, i=" + str(i) + ", total="
              + str(total_pages) + '\n')
        if result:
            collection.insert_many(result)
        i += 1


if __name__ == "__main__":
    client = connect_to_mongodb()
    db = client['antunedo']
    collection = db['offers']

    print('starting ...')
    for j in range(12, 52):
        immotype = str(j+1)
        total_pages = get_amount_of_pages(immotype)
        print("\nNouvel Immotype : " + immotype + ", avec un total de " + str(total_pages) + " pages\n\n")
        if total_pages > 1000:
            # TODO : filter this immo category into smaller elements
            print('DEAAAAAD')
        elif total_pages > 500:
            get_offers_by_immotype(collection, immotype, total_pages)
            # TODO : test if total_pages - 500 if right
            get_offers_by_immotype(collection, immotype, total_pages - 500, "desc")
        else:
            get_offers_by_immotype(collection, immotype, total_pages)

    client.close()
