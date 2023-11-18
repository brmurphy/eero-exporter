#!/usr/bin/env python
from argparse import ArgumentParser
from prometheus_client import start_http_server
from prometheus_client.core import GaugeMetricFamily, InfoMetricFamily, REGISTRY
import eero as eero_api
import time
import cookie_store
import sys
from datetime import datetime

class JsonCollector(object):
    def collect(self):
        print("connecting to eero api")
        account = eero_api_session.account()
        print("connected to eero api")
        for network in account['networks']['data']:

            metrics = {}
            label_names = ['network_id', 'network_name', 'network_display_name']
            eero_features = ["upnp", "ipv6", "thread", "sqm", "band_steering", "wpa3", "amazon_account_linked", "alexa_skill", "amazon_device_nickname", "backup_internet_enabled", "power_saving"]
            client_details_list = ["manufacturer"]

            # Creating Metric Families

            # Network-specific metrics
            metrics["ssid"] = InfoMetricFamily('eero_network_ssid', 'Current Eero Network SSID and Nickname, will always output 1 if detected', labels = label_names)
            metrics["supported_feature"] = GaugeMetricFamily('eero_network_feature_supported', 'If the Eero Network can support feature, output 1 if supported', labels = ['feature'] + label_names)
            metrics["wan_ip"] = InfoMetricFamily('eero_network_wan_ip', 'WAN IP for the Eero Network, should be your Public IP if you are in a double nat', labels = label_names)
            metrics["connection_mode"] = InfoMetricFamily('eero_network_connection', 'What the Eero Network is connected to', labels = label_names)
            metrics["dhcp"] = InfoMetricFamily('eero_network_dhcp', 'Configured DHCP Settings for the Eero Network', labels = label_names)
            metrics["dns"] = InfoMetricFamily('eero_network_dns', 'Configured DNS Settings for the Eero Network', labels = label_names)
            for feature in eero_features:
                metrics[feature] = GaugeMetricFamily('eero_network_' + feature, 'If ' + feature + ' is enabled, output 1 if enabled', labels=label_names)
            metrics["client_count"] = GaugeMetricFamily('eero_network_client_count', 'Total amount of clients connected to network', labels = label_names)
            metrics["upload_bandwidth"] = GaugeMetricFamily('eero_network_upload_bandwidth', 'Upload Speed in Bits per Second', labels = label_names, unit = "bps")
            metrics["download_bandwidth"] = GaugeMetricFamily('eero_network_download_bandwidth', 'Upload Speed in Bits per Second', labels = label_names, unit = "bps")
            metrics["bandwidth_last_test"] = GaugeMetricFamily('eero_network_bandwidth_last_test', 'Last time that bandwidth test was performed', labels = label_names)
            metrics["update_version"] = InfoMetricFamily('eero_network_update_version', 'Current Eero version of network', labels = label_names)
            metrics["has_update"] = GaugeMetricFamily('eero_network_update_available', 'Eero network has available update, 1 if true', labels = label_names)
            metrics["last_update"] = GaugeMetricFamily('eero_network_update_date', 'Datetime of last Eero update', labels = label_names)
            metrics["internet_health"] = GaugeMetricFamily('eero_network_internet_up', '1 if Eero reporting successful internet connection', labels = label_names)
            metrics["eero_health"] = GaugeMetricFamily('eero_network_up', '1 if Eero network reporting healthy', labels = label_names)
            metrics["public_ip"] = InfoMetricFamily('eero_network_public_ip', 'Public IP address of Eero network', labels = label_names)
            metrics["double_nat"] = GaugeMetricFamily('eero_network_double_nat', '1 if Eero detects that it detects it is behind an existing NAT', labels = label_names)
            metrics["premium_dns_enabled"] = GaugeMetricFamily('eero_network_premium_dns_enabled', '1 if Eero Secure Plus DNS settings are enabled', labels = label_names)
            metrics["premium_dns_policies"] = InfoMetricFamily('eero_network_premium_dns_policies', 'Premium DNS policies enabled on network', labels = label_names)
            metrics["homekit_enabled"] = GaugeMetricFamily('eero_network_homekit_enabled', '1 if Eero connected to Apple Homekit', labels = label_names)
            metrics["homekit_managed_network"] = GaugeMetricFamily('eero_network_homekit_managed_network_enabled', '1 if Homekit Managed Network is enabled on Eero Routers', labels = label_names)
            metrics["guest_ssid_enabled"] = GaugeMetricFamily('eero_network_guest_ssid_enabled', '1 if Guest Network is enabled', labels = label_names)
            metrics["guest_ssid"] = InfoMetricFamily('eero_network_guest_ssid', 'SSID of Guest Network', labels = label_names)
            metrics["last_reboot"] = GaugeMetricFamily('eero_network_last_restart', 'Time of last full network restart', labels = label_names)
            metrics["ddns_enabled"] = GaugeMetricFamily('eero_network_ddns_enabled', '1 if Dynamic DNS is enabled', labels = label_names)
            metrics["ddns_subdomain"] = InfoMetricFamily('eero_network_ddns_subdomain', 'Unique domain with public IP as A record', labels = label_names)

            # Eero-specific metrics
            eero_label_names = ["eero_id", "eero_name"] + label_names
            metrics["eero_count"] = GaugeMetricFamily('eero_network_eero_count', 'Amount of Eeros connected to network', labels=label_names)
            metrics["eero_model"] = InfoMetricFamily('eero_network_eero_model', 'Eero Model Name and Number', labels = eero_label_names)
            metrics["eero_mac"] = InfoMetricFamily('eero_network_eero_mac', 'Eero Router MAC Addresses', labels = eero_label_names)
            metrics["eero_mesh_connection_quality"] = GaugeMetricFamily('eero_network_eero_mesh_connection_quality', 'Connection quality of Eeros to mesh network as a percentage, gateway Eero will always be 100%', labels = eero_label_names)
            metrics['eero_mesh_connection_type'] = InfoMetricFamily('eero_network_eero_mesh_connection_type', 'If the connection type is either Wired or Wireless, Gateway Eero will always be WIRED', labels = eero_label_names)
            metrics['eero_gateway'] = GaugeMetricFamily('eero_network_eero_gateway', 'Outputs 1 if Gateway Eero', labels = eero_label_names)
            metrics['eero_status'] = GaugeMetricFamily('eero_network_eero_status', 'Outputs 1 if Eero is in a Good (green) Status', labels = eero_label_names)
            metrics["eero_client_count"] = GaugeMetricFamily('eero_network_eero_client_count', 'The amount of clients connected to Eero Router', labels = eero_label_names)
            metrics['eero_heartbeat'] = GaugeMetricFamily('eero_network_eero_heartbeat', '1 if Eero is passing heartbeat checks', labels = eero_label_names)
            metrics['eero_last_heartbeat'] = GaugeMetricFamily('eero_network_eero_last_heartbeat', 'Date and Time in Epoch of last successful Heartbeat', labels = eero_label_names)
            metrics['eero_wifi'] = GaugeMetricFamily('eero_network_eero_wifi_enabled', 'If wireless connectivity is enabled on the Eero, 1 if enabled', labels = eero_label_names)
            metrics['eero_wifi_bands'] = InfoMetricFamily('eero_network_eero_wifi_bands', 'Enabled Wireless Bands of Eero', labels = eero_label_names)
            metrics["eero_ipv4"] = InfoMetricFamily('eero_network_eero_ipv4', 'Eero Router IPv4 Address', labels = eero_label_names)
            metrics["eero_ipv6"] = InfoMetricFamily('eero_network_eero_ipv6', 'Eero Router IPv6 Address', labels = eero_label_names)
            metrics["eero_version"] = InfoMetricFamily('eero_network_eero_version', 'Current OS version of Eero', labels = eero_label_names)
            metrics["eero_last_reboot"] = GaugeMetricFamily('eero_network_eero_last_restart', 'Last restart of eero device, value does not update with full network restarts (see eero_network_last_restart)', labels = eero_label_names)

            # Client-specific metrics
            client_label_names = ["client_mac", "client_hostname", "client_display_name"] + eero_label_names
            metrics["client_details"] = InfoMetricFamily('eero_network_client_details', "miscellaneous collected details of connected clients", labels = client_label_names)
            metrics["client_ip"] = InfoMetricFamily('eero_network_client_ip', 'ip addresses of connected clients', labels = client_label_names)
            metrics["client_connected"] = GaugeMetricFamily('eero_network_client_connected', 'if client is currently connected to the network', labels = client_label_names)
            metrics["client_connection_type"] = InfoMetricFamily('eero_network_client_connection_type', 'how the client is connected to the network, generally either wired or wireless', labels = client_label_names)
            metrics["client_last_active"] = GaugeMetricFamily('eero_network_client_last_active', 'time when client was last active', labels = client_label_names)
            metrics["client_connection_strength"] = GaugeMetricFamily('eero_network_client_connection_strength', 'connection strength in dBm', labels = client_label_names, unit = "dBm")
            metrics["client_connection_quality"] = GaugeMetricFamily('eero_network_client_connection_quality', 'connection quality as a percentage, 1 is best quality. wired connections will not appear', labels = client_label_names)
            metrics["client_connection_wireless_frequency"] = GaugeMetricFamily('eero_network_client_connection_frequency', 'wireless frequency client is connected via', labels = client_label_names)
            metrics["client_rx_bandwidth"] = GaugeMetricFamily('eero_network_client_rx_bandwidth', 'client receive bandwidth in bits per second', labels = client_label_names, unit = "bps")
            metrics["client_tx_bandwidth"] = GaugeMetricFamily('eero_network_client_tx_bandwidth', 'client transmit bandwidth in bits per second', labels = client_label_names, unit = "bps")
            metrics["client_rx_connection_details"] = InfoMetricFamily('eero_network_client_connection_details', 'miscellaneous collected client receive connection details', labels = client_label_names)
            metrics["client_tx_connection_details"] = InfoMetricFamily('eero_network_client_connection_details', 'miscellaneous collected client transmit connection details', labels = client_label_names)
            metrics["client_connection_auth_type"] = InfoMetricFamily('eero_network_client_connection_auth', 'authentication method of the wireless device', labels = client_label_names)
            metrics["client_connection_channel"] = GaugeMetricFamily('eero_network_client_connection_channel', 'wireless channel that client is connected via', labels = client_label_names)
            metrics["client_wired_bandwidth"] = GaugeMetricFamily('eero_network_client_wired_bandwidth', 'bandwidth of wired client in bits per second', labels = client_label_names, unit = "bps")
            metrics["client_blacklisted"] = GaugeMetricFamily('eero_network_client_blacklisted', 'if client is blocked from connecting to the network, 1 if true', labels = client_label_names)
            metrics["client_paused"] = GaugeMetricFamily('eero_network_client_paused', 'if client is temporarily blocked from connecting to the network, 1 if true', labels = client_label_names)
            metrics["client_guest"] = GaugeMetricFamily('eero_network_client_guest', '1 if client is connected to guest network', labels = client_label_names)
            metrics["client_homekit"] = GaugeMetricFamily('eero_network_client_homekit', '1 if client is registered with homekit secure router network', labels = ["protection_mode"] + client_label_names)

            network_id = network['url'].split('/')[3]

            network_details = eero_api_session.networks(network['url'])
            network_clients = eero_api_session.devices(network['url'])

            # Global Labels and Values
            label_values = [network['url'].split('/')[3], network["name"], network["nickname_label"] if network["nickname_label"] != None else network["name"] ]

            metrics["ssid"].add_metric(label_values, value = {"ssid" : network["name"]})

            for feature in network_details["capabilities"]:
                metrics["supported_feature"].add_metric([feature] + label_values, 1 if network_details["capabilities"][feature]["capable"] else 0)

            metrics["wan_ip"].add_metric(label_values, value = {"wan_ip" : network_details["wan_ip"]})

            metrics["connection_mode"].add_metric(label_values, value = {"connection" : network_details["connection"]["mode"]})

            metrics["dhcp"].add_metric(label_values, value = {"dhcp_mode" : network_details["dhcp"]["mode"]})

            if network_details["dhcp"]["mode"] != "automatic":
                metrics["dhcp"].add_metric(label_values, value = {"dhcp_subnet_mask" : network_details["dhcp"]["custom"]["subnet_mask"]})
                metrics["dhcp"].add_metric(label_values, value = {"dhcp_subnet_ip" : network_details["dhcp"]["custom"]["subnet_ip"]})

            metrics["dns"].add_metric(label_values, value = {"dns_mode" : network_details["dns"]["mode"]})
            metrics["dns"].add_metric(label_values, value = {"dns_caching" : "true" if network_details["dns"]["caching"] else "false"})
            metrics["dns"].add_metric(label_values, value = {"dns_server" : ", ".join(network_details["dns"]["custom"]["ips"] if network_details["dns"]["mode"] == "custom" else network_details["dns"]["parent"]["ips"])})

            for feature in eero_features:
                metrics[feature].add_metric(label_values, 1 if network_details[feature] else 0)

            metrics["client_count"].add_metric(label_values, network_details["clients"]["count"])
            
            # converting to bits per second per Prometheus unit standards
            metrics["upload_bandwidth"].add_metric(label_values, network_details["speed"]["up"]["value"] * 1000000)
            metrics["download_bandwidth"].add_metric(label_values, network_details["speed"]["down"]["value"] * 1000000)
            metrics["bandwidth_last_test"].add_metric(label_values, datetime.timestamp(datetime.strptime(network_details["speed"]["date"], "%Y-%m-%dT%H:%M:%SZ")))

            metrics["update_version"].add_metric(label_values, value = {"version" : network_details["updates"]["target_firmware"]})
            metrics["has_update"].add_metric(label_values, 1 if network_details["updates"]["has_update"] else 0)
            metrics["last_update"].add_metric(label_values, datetime.timestamp(datetime.strptime(network_details["updates"]["last_update_started"], "%Y-%m-%dT%H:%M:%S.%fZ")))

            metrics["internet_health"].add_metric(label_values, 1 if network_details["health"]["internet"]["status"] == "connected" else 0)
            metrics["eero_health"].add_metric(label_values, 1 if network_details["health"]["eero_network"]["status"] == "connected" else 0)

            metrics["public_ip"].add_metric(label_values, value = {"ip" : network_details["ip_settings"]["public_ip"]})

            metrics["double_nat"].add_metric(label_values, 1 if network_details["ip_settings"]["double_nat"] else 0)

            metrics["premium_dns_enabled"].add_metric(label_values, 1 if network_details["premium_dns"]["dns_policies_enabled"] else 0)
            for policy in network_details["premium_dns"]["dns_policies"]:
                if network_details["premium_dns"]["dns_policies"][policy]:
                    metrics["premium_dns_policies"].add_metric(label_values, value = {"policy" : policy})

            metrics["last_reboot"].add_metric(label_values, datetime.timestamp(datetime.strptime(network_details["last_reboot"], "%Y-%m-%dT%H:%M:%S.%fZ")) if network_details["last_reboot"] != None else 0)

            if network_details["homekit"] != None:
                metrics["homekit_enabled"].add_metric(label_values, 1 if network_details["homekit"]["enabled"] else 0)
                metrics["homekit_managed_network"].add_metric(label_values, 1 if network_details["homekit"]["managedNetworkEnabled"] else 0)

            metrics["guest_ssid"].add_metric(label_values, value = {"ssid" : network_details["guest_network"]["name"]})
            metrics["guest_ssid_enabled"].add_metric(label_values, 1 if network_details["guest_network"]["enabled"] else 0)

            metrics["ddns_enabled"].add_metric(label_values, 1 if network_details["ddns"]["enabled"] else 0)
            metrics["ddns_subdomain"].add_metric(label_values, value = {"domain" : network_details["ddns"]["subdomain"]})

            metrics["eero_count"].add_metric(label_values, network_details["eeros"]["count"])

            for eero in network_details["eeros"]["data"]:
                eero_id = eero['url'].split('/')[3]
                eero_name = eero["location"]
                eero_label_values = [eero_id, eero_name] + label_values
                metrics["eero_model"].add_metric(eero_label_values, value = {"model" : eero["model"]})
                metrics["eero_model"].add_metric(eero_label_values, value = {"model_number" : eero["model_number"]})
                metrics["eero_mesh_connection_quality"].add_metric(eero_label_values, eero["mesh_quality_bars"]/5 if eero["mesh_quality_bars"] != None else 0)
                metrics["eero_mesh_connection_type"].add_metric(eero_label_values, value = {"connection" : eero["connection_type"] if eero["connection_type"] != None else "DISCONNECTED"})
                metrics["eero_gateway"].add_metric(eero_label_values, 1 if eero["gateway"] else 0)
                metrics["eero_status"].add_metric(eero_label_values, 1 if eero["status"] == "green" else 0)
                metrics["eero_client_count"].add_metric(eero_label_values, eero["connected_clients_count"])
                metrics["eero_heartbeat"].add_metric(eero_label_values, 1 if eero["heartbeat_ok"] else 0)
                metrics["eero_last_heartbeat"].add_metric(eero_label_values, datetime.timestamp(datetime.strptime(eero["last_heartbeat"], "%Y-%m-%dT%H:%M:%S.%fZ")))
                metrics['eero_wifi'].add_metric(eero_label_values, 1 if eero["provides_wifi"] else 0)
                # foreach instead of join?
                metrics["eero_wifi_bands"].add_metric(eero_label_values, value = {"band" : ", ".join(eero["bands"])})
                metrics["eero_mac"].add_metric(eero_label_values, value = {"mac_address" : ", ".join(eero["ethernet_addresses"] + eero["wifi_bssids"])})
                metrics["eero_ipv4"].add_metric(eero_label_values, value = {"ipv4_address" : eero["ip_address"]})
                ipv6_addresses = []
                for ipv6 in eero["ipv6_addresses"]:
                    ipv6_addresses.append(ipv6["address"])
                metrics["eero_ipv6"].add_metric(eero_label_values, value = {"ipv6_address" : ", ".join(ipv6_addresses)})
                metrics["eero_version"].add_metric(eero_label_values, value = {"version" : eero["os"]})
                metrics["eero_last_reboot"].add_metric(eero_label_values, datetime.timestamp(datetime.strptime(eero["last_reboot"], "%Y-%m-%dT%H:%M:%S.%fZ")) if eero["last_reboot"] != None else 0)

            for client in network_clients:
                client_label_values = [client["mac"], client["hostname"] if client["hostname"] != None else "", client["display_name"] if client["display_name"] != None else "", client["source"]["url"].split('/')[3], client["source"]["location"]] + label_values
                for detail in client_details_list:
                    if client[detail] != None:
                        metrics["client_details"].add_metric(client_label_values, value = {detail : client[detail]})

                for ip in client["ips"]:
                    metrics["client_ip"].add_metric(client_label_values, value = {"ip" : ip})

                metrics["client_connected"].add_metric(client_label_values, 1 if client["connected"] else 0)
                metrics["client_connection_type"].add_metric(client_label_values, value = {"connection" : client["connection_type"]})
                metrics["client_last_active"].add_metric(client_label_values, datetime.timestamp(datetime.strptime(client["last_active"], "%Y-%m-%dT%H:%M:%S.%fZ")))

                if client["wireless"]:
                    metrics["client_connection_strength"].add_metric(client_label_values, client["connectivity"]["signal"][:-4])
                    metrics["client_connection_quality"].add_metric(client_label_values, client["connectivity"]["score"])
                    metrics["client_connection_wireless_frequency"].add_metric(client_label_values, client["connectivity"]["frequency"])

                    metrics["client_rx_bandwidth"].add_metric(client_label_values, client["connectivity"]["rx_rate_info"]["rate_bps"] if client["connectivity"]["rx_rate_info"]["rate_bps"] != None else 0)
                    metrics["client_tx_bandwidth"].add_metric(client_label_values, client["connectivity"]["tx_rate_info"]["rate_bps"] if client["connectivity"]["tx_rate_info"]["rate_bps"] != None else 0)

                    for rx in client["connectivity"]["rx_rate_info"]:
                        if client["connectivity"]["rx_rate_info"][rx] != None:
                            if rx != "rate_bps":
                                metrics["client_rx_connection_details"].add_metric(client_label_values, value = {str(rx) : str(client["connectivity"]["rx_rate_info"][rx])})
                    for tx in client["connectivity"]["tx_rate_info"]:
                        if client["connectivity"]["tx_rate_info"][tx] != None:
                            if tx != "rate_bps":
                                metrics["client_tx_connection_details"].add_metric(client_label_values, value = {str(tx) : str(client["connectivity"]["tx_rate_info"][tx])})

                    metrics["client_connection_auth_type"].add_metric(client_label_values, value = {"auth" : client["auth"]})
                    metrics["client_connection_channel"].add_metric(client_label_values, client["channel"])
                if not client["wireless"]:
                    metrics["client_wired_bandwidth"].add_metric(client_label_values, client["connectivity"]["ethernet_status"]["speed"][1:] * 1000000)

                metrics['client_blacklisted'].add_metric(client_label_values, 0 if not client["blacklisted"] or client["blacklisted"] == None else 1)
                metrics['client_paused'].add_metric(client_label_values, 0 if not client["paused"] or client["paused"] == None else 1)

                metrics["client_guest"].add_metric(client_label_values, 1 if client["is_guest"] else 0)

                if client["homekit"]["registered"]:
                    metrics["client_homekit"].add_metric([client["homekit"]["protection_mode"]] + client_label_values, 1 if client["homekit"]["registered"] else 0)

            for metric in metrics:
                print("yielding " + metric)
                yield metrics[metric]

session = cookie_store.CookieStore('session.yml')
eero_api_session = eero_api.Eero(session)


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("-port", help="port to run the exporter on")
    args = parser.parse_args()

    if args.port:
        port = int(args.port)
    else:
        port = 9118
    REGISTRY.register(JsonCollector())
    print("starting http server")
    start_http_server(port)

    coll = JsonCollector()
    while True:
        coll.collect()
        time.sleep(1)
