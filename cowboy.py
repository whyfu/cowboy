import sys
import requests

def showHelp():
	print("cowboy yeehaw\n")
	print("Usage:\n\tpython cowboy.py %district_id% %start_date% [-o/a]")
	print("\nFlags:\n\t-o: show only available slots\n\t-a: show only 18+ slots")
	input()
	quit()

av_only = False
zoomer_only = False

district_id = str(sys.argv[1])
date = str(sys.argv[2])
heamders = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36 Edg/90.0.818.51'}
pog = requests.get('https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id={0}&date={1}'.format(district_id, date), headers=heamders)

for passed_args in sys.argv[3:]:
	if (passed_args[0] == '-'):
		for arg in passed_args[1:]:
			if (arg == 'a'): 
				zoomer_only = True
			elif (arg == 'o'):
				av_only = True
			else: 
				print("\nUnknown argument: '{0}'\n".format(arg))
				showHelp()
	else:
		print("\nInvalid usage.\n")
		showHelp()

centre_list = []
response_dict = pog.json()
av_boomer = 0
av_zoomer = 0
av_total = 0
av_sus = 0
av_centers = 0
for center in response_dict['centers']:
	print("Name of center:", center['name'])
	print("Address:", center['address'])
	sescount = 0
	is_av = False
	zoomer_slots = False
	boomer_slots = False
	for sus in center['sessions']:
		if (av_only):
			if (int(sus['available_capacity']) == 0):
				continue
		if (zoomer_only):
			if (int(sus['min_age_limit']) == 45):
				continue
		print("Date:", sus['date'])
		print("Vaccine:", sus['vaccine'])
		print("Slot times:", sus['slots'])
		print("Slots left:", sus['available_capacity'])
		print("Age limit:", sus['min_age_limit'])
		print("\n")
		sescount = sescount + 1
		if (int(sus['available_capacity']) != 0):
			is_av = True
			av_sus = av_sus + 1
			if (int(sus['min_age_limit']) == 45):
				boomer_slots = True
				av_boomer = av_boomer + int(sus['available_capacity'])
			else:
				av_zoomer = av_zoomer + int(sus['available_capacity'])
				zoomer_slots = True
	if (sescount == 0): print("\n[No sessions available] (check your filters)\n")
	if (is_av):
		av_centers = av_centers + 1
		if (zoomer_only):
			if (zoomer_slots): centre_list.append(center['name'])
		else: centre_list.append(center['name'])

av_total = av_boomer + av_zoomer
print("Start Date: {0}".format(date))
if (av_total == 0):
	print("\nEh, no slots available. Check back soon!\n")
else:
	print("\n{0} slot(s) available, in {1} unique session(s) across {2} center(s).".format(av_total, av_sus, av_centers))
	print("{0} slot(s) for 18+ year olds, {1} slot(s) for 45+ year olds.".format(av_zoomer, av_boomer))
	print("\nCheck these centres: ", centre_list)
