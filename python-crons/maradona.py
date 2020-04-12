#!/usr/bin python3.7
# -*- coding: utf-8 -*-
import sys
import time
from random import randint

from lib.mongoConnector import connect_to_mongodb, get_last_maradona_execution, update_geographical_filter_options
from lib.queryBuilder import last_inserted_offers
from lib.utils import add_fields_to_offer


def sniffer(last_exec_time, mongo_client):
    time.sleep(randint(0, 10))
    begin_time = time.time()
    offers_collection = mongo_client['antunedo']['offers']
    logs_collection = mongo_client['antunedo']['logs']
    avg_collection = mongo_client['antunedo']['average_prices']

    page = 1
    cpt = 0
    already_added_cpt = 0
    new_offers_cpt = 0
    total_pages = 501
    while page < total_pages and page < 501:
        next_page, total_pages = last_inserted_offers(page, last_exec_time)
        for offer in next_page:
            if offers_collection.find_one({'id': offer['id']}) is not None:
                already_added_cpt += 1
            else:
                new_offers_cpt += 1
                add_fields_to_offer(offer, int(begin_time), avg_collection)
                update_geographical_filter_options(mongo_client, offer)
                offers_collection.insert_one(offer)
                print('New offer : ' + str(offer['id']))
            cpt += 1
        page += 1
    print(str(cpt) + " offers were sniffed, " + str(new_offers_cpt) + " are new offers.")
    logs_collection.insert_one({
        "start_time": int(begin_time),
        "already_added_offers": already_added_cpt,
        "new_offers": new_offers_cpt,
        "duration": round(time.time() - begin_time, 2)
    })
    return


if __name__ == "__main__":
    client = connect_to_mongodb()
    if len(sys.argv) > 1:
        timespan = int(time.time()) - int(sys.argv[1])
    else:
        timespan = get_last_maradona_execution(client) - 3600
    sniffer(timespan, client)

    client.close()
