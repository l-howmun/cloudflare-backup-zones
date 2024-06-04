import requests
import time
import os

# Replace this with your Cloudflare API token
# will require ZONE - READ and DNS - READ permission for the API token
CLOUDFLARE_API_TOKEN = 'REPLACE-YOUR-CLOUDFLARE-API-TOKEN-HERE'
BASE_URL = 'https://api.cloudflare.com/client/v4'
# cloudflare rate limit: 1200 requests per five minutes per user
DELAY_SECONDS = 1  # Adjust the delay as needed


# Create a session
session = requests.Session()
session.headers.update({
    'Authorization': f'Bearer {CLOUDFLARE_API_TOKEN}',
    'Content-Type': 'application/json'
})

def get_zones():
    zones = []
    url = f'{BASE_URL}/zones'
    while url:
        response = session.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        result = response.json()
        zones.extend(result['result'])
        url = result.get('result_info', {}).get('next', None)
    return zones

def export_zone(zone_id, zone_name):
    url = f'{BASE_URL}/zones/{zone_id}/dns_records/export'
    response = session.get(url)
    response.raise_for_status()  # Raise an exception for HTTP errors
    zone_file_content = response.text

    # Save to a file
    filename = f'zone_backups/{zone_name}.txt'
    with open(filename, 'w') as file:
        file.write(zone_file_content)
    print(f'Zone file for {zone_name} saved as {filename}')

def main():
    zones = get_zones()
    for zone in zones:
        zone_id = zone['id']
        zone_name = zone['name']
        print(f'Exporting zone: {zone_name}')
        export_zone(zone_id, zone_name)
        time.sleep(DELAY_SECONDS)  # Introduce a delay between requests

if __name__ == '__main__':
    main()
