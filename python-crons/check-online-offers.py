#!/usr/bin python3.7
# -*- coding: utf-8 -*-
from pymongo.errors import DuplicateKeyError

from lib.mongoConnector import connect_to_mongodb, pop_offers_already_saved
from lib.queryBuilder import query_immo_offers, get_amount_of_pages


def get_offers_ids(immotype, total_pages, sort="asc"):
    ids = []
    if total_pages == 0:
        return
    i = 0
    while i <= total_pages and i <= 500:
        result = query_immo_offers(i, immotype, sort)
        print("Processing data... " + "{0:.2f}".format((i / total_pages) * 100) + "%, i=" + str(i) + ", total="
              + str(total_pages) + '\n')
        if result:
            for k in result:
                ids.append(k['id'])
        i += 1
    return ids


if __name__ == "__main__":
    client = connect_to_mongodb()
    db = client['antunedo']
    mongo_collection = db['offers']
    online_offers = []
    categories_done = []

    print('starting ...')
    for j in range(0, 52):
        immotype_id = str(j + 1)
        total_page_count = get_amount_of_pages(immotype_id)
        print("\nNouvel Immotype : " + immotype_id + ", avec un total de " + str(total_page_count) + " pages\n\n")
        if total_page_count > 0:
            if total_page_count > 1000:
                # TODO : filter this immo category into smaller elements
                print('DEAAAAAD    ---    immotype ID : ' + immotype_id + '\n\n')
            elif total_page_count > 500:
                online_offers += get_offers_ids(immotype_id, total_page_count)
                online_offers += get_offers_ids(immotype_id, total_page_count - 500, "desc")
                categories_done.append(int(immotype_id))
            else:
                online_offers += get_offers_ids(immotype_id, total_page_count)
                categories_done.append(int(immotype_id))
            mongo_collection.update_many({'id': {'$in': online_offers}}, {'$set': {'is_online': True}})
            print(online_offers)
            online_offers = []
    print(categories_done)
    client.close()
