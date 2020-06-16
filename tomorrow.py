import urllib3
import json
import os
from datetime import datetime
import clipboard
import time
import config
import location

GPS_COORDS = f"{loc['latitude']}, {loc['longitude']}"
DARKSKY_API_KEY = config.DARKSKY_API_KEY

# Time calculations 

time = datetime.now()
month = str(time.month).zfill(2) if len(str(time.month)) == 1 else str(time.month)
day = str(time.day+1).zfill(2) if len(str(time.day+1)) == 1 else str(time.day+1)
day_after = str(time.day+2).zfill(2) if len(str(time.day+2)) == 1 else str(time.day+2)
tomorrow_str = f"{time.year}-{month}-{day} 12:00:00"
day_after_str = f"{time.year}-{month}-{day_after} 12:00:00"
tomorrow_dt = round(datetime.timestamp(datetime.strptime(tomorrow_str, '%Y-%m-%d %H:%M:%S')))
day_after_dt = round(datetime.timestamp(datetime.strptime(day_after_str, '%Y-%m-%d %H:%M:%S')))
tomorrow = f",{tomorrow_dt}"
day_after_full = f",{day_after_dt}"

def get_current_conditions(time):
	api_conditions_url = "https://api.darksky.net/forecast/" + DARKSKY_API_KEY + "/" + GPS_COORDS + time + "?exclude=currently,flags"
	try:
		http = urllib3.PoolManager()
		r = http.request('GET', api_conditions_url)
	except:
		return []
	json_currently = r.data
	return json.loads(json_currently)
	
def moon_icon(moon_phase):
	if moon_phase < .06:
		return "Tomorrow is a new moon"
	if moon_phase < .125 and moon_phase >= 0.06:
		return "Tomorrow, the moon is a waxing crescent. "
	if moon_phase < .25 and moon_phase >= 0.125:
		return "Tomorrow, the moon is in its first quarter. "
	if moon_phase < .48 and moon_phase >= 0.25:
		return "Tomorrow, the moon is a waxing gibbbous. "
	if moon_phase < .52 and moon_phase >= 0.48:
		return "Tomorrow, is a full moon."
	if moon_phase < .625 and moon_phase >= 0.52:
		return "Tomorrow, the moon is a waning gibbous. "
	if moon_phase < .75 and moon_phase >= 0.625:
		return "Tomorrow, the moon is in its last quarter. "
	if moon_phase < 1 and moon_phase >= 0.75:
		return "Tomorrow, the moon is a waning crescent. "


		
curr_conditions = get_current_conditions(tomorrow)

hours = [i for i in [j['time'] for j in curr_conditions['hourly']['data']]]

sunset = curr_conditions['daily']['data'][0]['sunsetTime']

sunset_min = str(datetime.fromtimestamp(sunset).minute).zfill(2) if len(str(datetime.fromtimestamp(sunset).minute)) == 1 else str(datetime.fromtimestamp(sunset).minute)

day_after_conditions = get_current_conditions(day_after_full)
sunrise = day_after_conditions['daily']['data'][0]['sunriseTime']
sunrise_min = str(datetime.fromtimestamp(sunrise).minute).zfill(2) if len(str(datetime.fromtimestamp(sunrise).minute)) == 1 else str(datetime.fromtimestamp(sunrise).minute)
moon_phase = moon_icon(curr_conditions['daily']['data'][0]['moonPhase'])

remaining_hours = [i for i in hours if sunset < i]
next_hours = [round(datetime.timestamp(datetime.strptime(f"{time.year}-{month}-{day_after} {str(i).zfill(2)}:00:00", '%Y-%m-%d %H:%M:%S'))) for i in range(10) if round(datetime.timestamp(datetime.strptime(f"{time.year}-{month}-{day_after} {str(i).zfill(2)}:00:00", '%Y-%m-%d %H:%M:%S'))) < sunrise]
for next_hour in next_hours:
	remaining_hours.append(next_hour)
cloud_list = [(datetime.fromtimestamp(hour['time']).hour,str(round(hour['cloudCover']*100))+"%") for hour in [i for i in curr_conditions['hourly']['data']] if hour['time'] in remaining_hours and hour['cloudCover'] <= 0.1]

other_clouds = [(datetime.fromtimestamp(hour['time']).hour,str(round(hour['cloudCover']*100))+"%") for hour in [i for i in day_after_conditions['hourly']['data']] if hour['time'] in remaining_hours and hour['cloudCover'] <= 0.1]

for other_cloud in other_clouds:
	cloud_list.append(other_cloud)
	
output = ""
if len(cloud_list) == 0:
	output = "No, the skies are far too cloudy tomorrow. Try again the next day."
else:
	output += "Yes, you can observe tomorrow. "
	for tupl in cloud_list:
		if tupl[0] > 12:
			output += f"Cloud cover is {tupl[1]} at {tupl[0] % 12} PM. "
		elif tupl[0] == 0:
			output += f"Cloud cover is {tupl[1]} at 12 AM. "
		else:
			output += f"Cloud cover is {tupl[1]} at {tupl[0]} AM. "
	output += f"Sunset tomorrow is at {datetime.fromtimestamp(sunset).hour}:{sunset_min} PM. "
	output += moon_phase
	output += f"Moon presence is at {round(curr_conditions['daily']['data'][0]['moonPhase']*100)}%. "	
	output += f"Sunrise is at {datetime.fromtimestamp(sunrise).hour}:{sunrise_min} AM on the following day."


clipboard.set('{}'.format(output))


