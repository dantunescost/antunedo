import time

import slack

token = "xoxp-631514766916-620592331859-753712754641-47ae8f220bc6fb86591961d3812e79e4"
slack_client = slack.WebClient(token=token)


def send_slack_alert(channel, title, url, price, surface, price_per_m2, country, city, magic_ratio, photo_url):
    attachments = [
        {
            "fallback": "Required plain-text summary of the attachment.",
            "color": "#0346ff",
            "title": title + " avec un prix inférieur à de la moyenne du marché à été "
                     "détectée",
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
                }],
            "thumb_url": photo_url,
            "footer": "Invest-AF ",
            "footer_icon": "https://i2.wp.com/www.andreasreiterer.at/wp-content/uploads/2017/11/"
                           "react-logo.jpg?resize=825%2C510&ssl=1",
            "ts": int(time.time())
        }
    ]
    if country != "":
        attachments[0]['fields'].append({
            "title": "Pays",
            "value": country,
            "short": True
        })
    if country != " ville inconnue":
        attachments[0]['fields'].append({
            "title": "Ville",
            "value": city,
            "short": True
        })
    slack_client.chat_postMessage(
        channel=channel,
        attachments=attachments
    )
