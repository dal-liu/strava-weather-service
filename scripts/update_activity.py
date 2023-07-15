import sys
import utils.strava_api as strava_api
from utils.openmeteo_api import get_weather_at_point

id = sys.argv[1]
name, start_date, start_latlng = strava_api.get_name_dt_and_latlng(id)
if len(start_latlng) == 2:
    icon, description = get_weather_at_point(start_latlng[0], start_latlng[1], start_date)
    title = icon + ' ' + name
    print(f'Updating activity...')
    response = strava_api.update_activity(id, description, title)
    print(response)
