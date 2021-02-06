#!/usr/bin/env python
from argparse import ArgumentParser
from prometheus_client import start_http_server
from prometheus_client.core import GaugeMetricFamily, REGISTRY
import eero
import time
import cookie_store


class JsonCollector(object):
    def collect(self):
        account = eero.account()
        for network in account['networks']['data']:
            network_details = eero.networks(network['url'])
            network_speed = network_details['speed']

            id = network['url'].split('/')[3]
            metric1 = GaugeMetricFamily('eero_speed_upload_mbps', 'Current service response upload (Mbps)', labels=['id'])
            metric1.add_metric([id], value=network_speed['up']['value'])
            yield metric1
            metric2 = GaugeMetricFamily('eero_speed_download_mbps', 'Current service response download (Mbps)', labels=['id'])
            metric2.add_metric([id], value=network_speed['down']['value'])
            yield metric2

            network_health = network_details['health']
            metric3 = GaugeMetricFamily('eero_health_status', 'Current connection status', labels=['url', 'source'])
            metric3.add_metric([id, 'internet'], 1 if network_health['internet']['status'] == 'connected' else 0)
            metric3.add_metric([id, 'eero_network'], 1 if network_health['eero_network']['status'] == 'connected' else 0)
            yield metric3

            network_clients = network_details['clients']
            metric4 = GaugeMetricFamily('eero_clients_count', 'Current count of clients', labels=['id'])
            metric4.add_metric([id], network_clients['count'])
            yield metric4


session = cookie_store.CookieStore('session.yml')
eero = eero.Eero(session)


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("-port", help="port to run the exporter on")
    args = parser.parse_args()

    if args.port:
        port = int(args.port)
    else:
        port = 9118
    REGISTRY.register(JsonCollector())
    start_http_server(port)

    coll = JsonCollector()
    while True:
        coll.collect()
        time.sleep(1)
