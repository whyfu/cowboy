# dump state/district metadate from cowin server lol
import requests

print("dumping...")
sta_dump = open("states.json", "w")
dis_dump = open("districts.json", "w")
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36 Edg/90.0.818.51'}
states_response = requests.get('https://cdn-api.co-vin.in/api/v2/admin/location/states', headers=header)
states = states_response.json()

sta_dump.write(str(states))

for sta in states['states']:
	dis_response = requests.get('https://cdn-api.co-vin.in/api/v2/admin/location/districts/{0}'.format(sta['state_id']), headers=header)
	districts = dis_response.json()
	dis_dump.write(str(districts))

print("done.")