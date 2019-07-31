#!/usr/bin python3.7
# -*- coding: utf-8 -*-
import time

from lib.mongoConnector import connect_to_mongodb, get_last_maradona_execution
from lib.queryBuilder import last_inserted_offers
from lib.utils import add_fields_to_offer


def sniffer():
    begin_time = time.time()
    client = connect_to_mongodb()
    offers_collection = client['antunedo']['offers']
    logs_collection = client['antunedo']['logs']
    avg_collection = client['antunedo']['average_prices']

    page = 1
    cpt = 0
    already_added_cpt = 0
    new_offers_cpt = 0
    total_pages = 501
    last_exec_time = get_last_maradona_execution(client)
    while page < total_pages and page < 501:
        next_page, total_pages = last_inserted_offers(page, last_exec_time)
        for offer in next_page:
            print(cpt)
            if offers_collection.find_one({'id': offer['id']}) is not None:
                already_added_cpt += 1
                print('Already added')
            else:
                new_offers_cpt += 1
                add_fields_to_offer(offer, int(begin_time), avg_collection)
                offers_collection.insert_one(offer)
                print('New offer')
            cpt += 1
        page += 1
    logs_collection.insert_one({
        "start_time": int(begin_time),
        "already_added_offers": already_added_cpt,
        "new_offers": new_offers_cpt,
        "duration": round(time.time() - begin_time, 2)
    })

    client.close()
    return


if __name__ == "__main__":
    sniffer()
