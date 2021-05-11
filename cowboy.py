import sys
import requests
import winsound
import time

def showHelp():
	print("cowboy yeehaw\n")
	print("Usage:\n\tpython cowboy.py %district_id% %start_date% [-o/a]")
	print("\nFlags:\n\t-o: show only available slots")
	input()
	quit()

av_only = False
extrovert = False
beep = False
loops = 1
do_loop = False
stime = 10
i = 3
beepfor = 'n'

for passed_args in sys.argv[3:]:
	if (passed_args[0] == '-'):
		for arg in passed_args[1:]:
			if (arg == 'o'):
				av_only = True
			elif (arg == 'v'):
				extrovert = True
			elif (arg == 'b'):
				beep = True
				beepfor = sys.argv[i+1]
			elif (arg == 'l'):
				do_loop = True
				loops = int(sys.argv[i+1])
			elif (arg == 't'):
				stime = int(sys.argv[i+1])
			else: 
				print("\nUnknown argument: '{0}'\n".format(arg))
				showHelp()
	i = i+1

district_id = str(sys.argv[1])
date = str(sys.argv[2])

heamders = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36 Edg/90.0.818.51'}
for k in range(0, loops):
	pog = requests.get('https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id={0}&date={1}'.format(district_id, date), headers=heamders)

	boomer_list = []
	zoomer_list = []
	response_dict = pog.json()
	av_boomer = 0
	av_zoomer = 0
	av_total = 0
	av_sus = 0
	for center in response_dict['centers']:
		if (extrovert):
			print("Name of center:", center['name'])
			print("Address:", center['address'])
		bsus_list = []
		zsus_list = []
		for sus in center['sessions']:
			if (av_only):
				if (int(sus['available_capacity']) == 0):
					continue
			if (extrovert):
				print("Date:", sus['date'])
				print("Vaccine:", sus['vaccine'])
				print("Slot times:", sus['slots'])
				print("Slots left:", sus['available_capacity'])
				print("Age limit:", sus['min_age_limit'])
				print("")
			if (int(sus['available_capacity']) != 0):
				if (int(sus['min_age_limit']) == 45):
					bsus_list.append(sus['date'])
					av_boomer = av_boomer + int(sus['available_capacity'])
				else:	
					zsus_list.append(sus['date'])
					av_zoomer = av_zoomer + int(sus['available_capacity'])
		if(bsus_list): 
			boomer_list.append((center['name'], bsus_list))
			av_sus = av_sus + len(bsus_list)
		if(zsus_list):
			zoomer_list.append((center['name'], zsus_list))
			av_sus = av_sus + len(zsus_list)
		if (not bsus_list and not zsus_list and extrovert): print("[No slots available]\n")

	av_total = av_boomer + av_zoomer
	av_centers = len(boomer_list) + len(zoomer_list)
	if (do_loop):
		print("\n[Iteration {0} of {1}]".format(k+1, loops))
	print("\nFor 7 days from {0}".format(date))
	if (av_total == 0):
		print("\nEh, no slots available. Check back soon!\n")
	else:
		print("\n{0} slot(s) available, in {1} unique session(s) across {2} center(s).".format(av_total, av_sus, av_centers))
		print("{0} slot(s) for 18+ year olds, {1} slot(s) for 45+ year olds.".format(av_zoomer, av_boomer))
		if (boomer_list): 
			print("\nCheck these centers for 45+:", boomer_list)
			if (beepfor == 'b'): 
				print("Playing notification sound...") 
				winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
		if (zoomer_list): 
			print("\nCheck these centers for 18+:", zoomer_list)
			if (beepfor == 'z'):
				print("Playing notification sound...") 
				winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
	if(do_loop and (k+1 != loops)):
		print("Sleeping for {0} seconds...\nPress Ctrl+C to terminate".format(stime))
		time.sleep(stime)
