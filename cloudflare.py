#!/usr/bin/env python3
import CloudFlare
import config
import urllib.parse
import requests
import time
import socket

def update_cloudflare(netloc):
    ip, port = netloc.split(':')
    ip = socket.gethostbyname(ip)
    cf = CloudFlare.CloudFlare(token=config.CLOUDFLARE_TOKEN)
##    dns_records = cf.zones.dns_records.get(
##        CLOUDFLARE_ZONE, params={'name':''}
##    )
##    return dns_records
    r = cf.zones.dns_records.patch(
        config.CLOUDFLARE_ZONE,
        config.A_RECORD,
        data={
            'content':ip
            }
        )
    r2 = cf.zones.dns_records.patch(
        config.CLOUDFLARE_ZONE,
        config.SRV_RECORD,
        data={
            'data':{
                'port':port
                }
            }
        )

def get_tunnel():
    try:
        r=requests.get("http://127.0.0.1:4040/api/tunnels")
        for tunnel in r.json()['tunnels']:
            current_tunnel = urllib.parse.urlparse(tunnel['public_url'])
            if current_tunnel.scheme == 'tcp':
                return current_tunnel.netloc
    except:
        return None

tunnel = get_tunnel()
for attempt in range(5):
    if tunnel:
        update_cloudflare(tunnel)
        break
    print("Retrying in "+str(5+(attempt*5))+" seconds")
    time.sleep(5+(attempt*5))
    tunnel = get_tunnel()
