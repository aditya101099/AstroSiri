import urllib3
import json
import os
from datetime import datetime
import clipboard
import time
import location 
import webbrowser

GPS_COORDS = f"{loc['latitude']}, {loc['longitude']}"
DARKSKY_API_KEY = "9b88e268bff31516691599141aefa11c"



def get_current_conditions():
	api_conditions_url = "https://api.darksky.net/forecast/" + DARKSKY_API_KEY + "/" + GPS_COORDS + "?units=auto"
	try:
		http = urllib3.PoolManager()
		r = http.request('GET', api_conditions_url)
	except:
		return []
	json_currently = r.data
	return json.loads(json_currently)
	
def moon_icon(moon_phase):
	if moon_phase < .06:
		return "Tonight is a new moon"
	if moon_phase < .125 and moon_phase >= 0.06:
		return "Tonight, the moon is a waxing crescent. "
	if moon_phase < .25 and moon_phase >= 0.125:
		return "Tonight, the moon is in its first quarter. "
	if moon_phase < .48 and moon_phase >= 0.25:
		return "Tonight, the moon is a waxing gibbbous. "
	if moon_phase < .52 and moon_phase >= 0.48:
		return "Tonight, is a full moon."
	if moon_phase < .625 and moon_phase >= 0.52:
		return "Tonight, the moon is a waning gibbous. "
	if moon_phase < .75 and moon_phase >= 0.625:
		return "Tonight, the moon is in its last quarter. "
	if moon_phase < 1 and moon_phase >= 0.75:
		return "Tonight, the moon is a waning crescent. "


		
curr_conditions = get_current_conditions()
hours = [i for i in [j['time'] for j in curr_conditions['hourly']['data']]]

sunset = curr_conditions['daily']['data'][0]['sunsetTime']

sunset_min = str(datetime.fromtimestamp(sunset).minute) if len(str(datetime.fromtimestamp(sunset).minute)) > 1 else "0" + str(datetime.fromtimestamp(sunset).minute)

sunrise = curr_conditions['daily']['data'][1]['sunriseTime']

sunrise_min = str(datetime.fromtimestamp(sunrise).minute) if len(str(datetime.fromtimestamp(sunrise).minute)) > 1 else "0" + str(datetime.fromtimestamp(sunrise).minute)

today = datetime.fromtimestamp(hours[0]).day
moon_phase = moon_icon(curr_conditions['daily']['data'][0]['moonPhase'])

relevant_hours = [i for i in hours if sunset < i and i <= sunrise]

cloud_list = [(datetime.fromtimestamp(hour['time']).hour,str(round(hour['cloudCover']*100))+"%") for hour in [i for i in curr_conditions['hourly']['data']] if hour['time'] in relevant_hours]


output = "Cloud cover is "
for tupl in cloud_list:
	if tupl[0] > 12:
		output += f"{tupl[1]} at {tupl[0] % 12} PM. "
	elif tupl[0] == 0:
		output += f"{tupl[1]} at 12 AM. "
	else:
		output += f"{tupl[1]} at {tupl[0]} AM. "


clipboard.set('{}'.format(output))
url = "shortcuts://"
webbrowser.open(url)
