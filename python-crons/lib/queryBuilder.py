import requests
import json

from lib.utils import get_time_string


def query_immo_offers(page, immotype, sort):
    url = "https://www.athome.lu/portal-srp/api/v1/search"
    sort_field = "inserted|" + sort
    body_data = {
        "apireq": {
            "site": "lu_at_home",
            "page": page,
            "size": 20,
            "sort": [sort_field],
            "fgroup": "srp",
            "query": [
                {
                    "where": [],
                    "filters": {
                        "immotype_id": [immotype],
                        "is_old_build": True,
                        "transaction.type": "buy"
                    },
                    "modifiers": {
                        "with_child": True,
                        "apply_to_child": True,
                        "with_characteristic": True,
                        "with_agencies": True
                    },
                    "seo": []
                }
            ],
            "aggregate": [
                "last_inserted@20190331T220000Z"
            ]
        },
        "queryFilters": {
            "tr": "buy"
        },
        "domain": "athome.lu",
        "locale": "fr",
        "uri": "/vente"
    }
    payload = json.dumps(body_data)
    headers = {
        'Content-Type': "application/json",
        'Accept': "*/*",
        'Origin': "https://www.athome.lu",
        'Referer': "https://www.athome.lu/vente",
        'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/73.0.3683.103 Safari/537.36",
        'cache-control': "no-cache"
    }

    response = requests.request("POST", url, data=payload, headers=headers)
    if response is None:
        print(payload)
        return []
    return response.json()['list']


def get_amount_of_pages(immotype):
    url = "https://www.athome.lu/portal-srp/api/v1/search"

    body_data = {
        "apireq": {
            "site": "lu_at_home",
            "page": 1,
            "size": 20,
            "sort": [],
            "fgroup": "srp",
            "query": [
                {
                    "where": [],
                    "filters": {
                        "immotype_id": [immotype],
                        "is_old_build": True,
                        "transaction.type": "buy"
                    },
                    "modifiers": {
                        "with_child": True,
                        "apply_to_child": True,
                        "with_characteristic": True,
                        "with_agencies": True
                    },
                    "seo": []
                }
            ],
            "aggregate": [
                "last_inserted@20190331T220000Z"
            ]
        },
        "queryFilters": {
            "tr": "buy"
        },
        "domain": "athome.lu",
        "locale": "fr",
        "uri": "/vente"
    }
    payload = json.dumps(body_data)
    headers = {
        'Content-Type': "application/json",
        'Accept': "*/*",
        'Origin': "https://www.athome.lu",
        'Referer': "https://www.athome.lu/vente",
        'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/73.0.3683.103 Safari/537.36",
        'cache-control': "no-cache"
    }

    response = requests.request("POST", url, data=payload, headers=headers)

    return response.json()['paginator']['totalPages']


def last_inserted_offers(page, timestamp):
    time_string = get_time_string(timestamp)
    url = "https://www.athome.lu/portal-srp/api/v1/search"
    body_data = {
        "apireq": {
            "site": "lu_at_home",
            "page": page,
            "size": 20,
            "sort": ["inserted|asc"],
            "fgroup": "srp",
            "query": [
                {
                    "where": [],
                    "filters": {
                        "is_old_build": True,
                        "transaction.type": "buy",
                        "inserted": {"gte": time_string}
                    },
                    "modifiers": {
                        "with_child": True,
                        "apply_to_child": True,
                        "with_characteristic": True,
                        "with_agencies": True
                    },
                    "seo": []
                }
            ],
            "aggregate": [
                "last_inserted@" + time_string
            ]
        },
        "queryFilters": {
            "tr": "buy"
        },
        "domain": "athome.lu",
        "locale": "fr",
        "uri": "/vente"
    }
    payload = json.dumps(body_data)
    headers = {
        'Content-Type': "application/json",
        'Accept': "*/*",
        'Origin': "https://www.athome.lu",
        'Referer': "https://www.athome.lu/vente",
        'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/73.0.3683.103 Safari/537.36",
        'cache-control': "no-cache"
    }

    response = requests.request("POST", url, data=payload, headers=headers)
    if response is None:
        print(payload)
        return []
    return response.json()['list'], response.json()['paginator']['totalPages']
