import sys
import utils.strava_api as strava_api
from utils.noaa_weather import get_weather_at_point

id = sys.argv[1]
end_latlng = strava_api.get_latlng(id)
if len(end_latlng) == 2:
    description = get_weather_at_point(end_latlng[0], end_latlng[1])
    print(f'Updating activity with {description}...')
    response = strava_api.update_activity(id, description)
    print(response)
else:
    print('Activity did not contain map, did not update activity')
