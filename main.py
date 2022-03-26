import CloudFlare

CLOUDFLARE_TOKEN = input("Cloudflare token: ")
CLOUDFLARE_ZONE = input("Cloudflare zone: ")

def update_cloudflare(ip,port):
    cf = CloudFlare.CloudFlare(token=CLOUDFLARE_TOKEN)
    dns_records = cf.zones.dns_records.get(
        CLOUDFLARE_ZONE, params={'name':''}
    )
    return dns_records
