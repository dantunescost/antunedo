import configparser
import os
import time

import slack

path = os.path.dirname(os.path.abspath(__file__))
config = configparser.ConfigParser()
config.read(path + '''/../config/configuration.cfg''')

token = config['SLACK']['token']
slack_client = slack.WebClient(token=token)


def send_slack_alert(channel, title, url, price, surface, price_per_m2, offer_id, amount_of_offer_for_average,
                     magic_ratio, photo_url):
    attachments = [
        {
            "fallback": "Offer alert.",
            "color": "#0346ff",
            "title": title,
            "title_link": url,
            "fields": [
                {
                    "title": "Prix",
                    "value": "{:,}".format(price) + " €",
                    "short": True
                },
                {
                    "title": "Surface",
                    "value": str(surface) + " m²",
                    "short": True
                },
                {
                    "title": "Prix au m²",
                    "value": "{0:.2f}".format(price_per_m2) + " €/m²",
                    "short": True
                },
                {
                    "title": "Ratio / prix du marché",
                    "value": "{0:.2f}".format(magic_ratio) + " %",
                    "short": True
                },
                {
                    "title": "Identifiant",
                    "value": str(offer_id),
                    "short": True
                },
                {
                    "title": "Pertinence de la moyenne",
                    "value": str(amount_of_offer_for_average) + " biens utilisés",
                    "short": True
                }
            ],
            "actions": [
                {
                    "type": "button",
                    "text": "Lien vers offre :house_with_garden:",
                    "url": url
                },
                {
                    "type": "button",
                    "text": "Lien PDF :inbox_tray:",
                    "url": "https://www.athome.lu/annonce/downloadpdf/id/" + str(offer_id) + "/format/portrait/lang/fr"
                }
            ],
            "thumb_url": photo_url,
            "footer": "Invest-AF ",
            "footer_icon": "https://i2.wp.com/www.andreasreiterer.at/wp-content/uploads/2017/11/"
                           "react-logo.jpg?resize=825%2C510&ssl=1",
            "ts": int(time.time())
        }
    ]
    slack_client.chat_postMessage(
        channel=channel,
        attachments=attachments
    )