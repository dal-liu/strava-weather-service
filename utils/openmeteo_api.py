from datetime import datetime

import emoji
import requests


def get_weather_at_point(lat: int, lon: int, dt: str) -> tuple[str, str]:
    """Takes latitude and longitude and returns a string with a brief description of the weather at that location."""

    date_time = datetime.strptime(dt, "%Y-%m-%dT%H:%M:%SZ")

    base_url = "https://api.open-meteo.com/v1/forecast"
    date = date_time.strftime("%Y-%m-%d")
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": "temperature_2m,relativehumidity_2m,apparent_temperature,weathercode,windspeed_10m,winddirection_10m,is_day",
        "temperature_unit": "fahrenheit",
        "windspeed_unit": "mph",
        "timezone": "GMT",
        "start_date": date,
        "end_date": date,
    }

    # get the observation from Open-Meteo
    # if there is an error, return nothing
    response = requests.get(base_url, params=params)
    if response.status_code == 400:
        print("API request error")
        return ("", "")
    observation = response.json().get("hourly")
    if not observation:
        print("Weather key error")
        return ("", "")

    # first get the hour of the activity
    time = date_time.hour

    # extract relevant information from response
    condition, icon = _get_condition_and_icon(
        observation.get("weathercode")[time], observation.get("is_day")[time]
    )
    temperature = round(observation.get("temperature_2m")[time])
    feels_like = round(observation.get("apparent_temperature")[time])
    humidity = round(observation.get("relativehumidity_2m")[time])
    wind_speed = round(observation.get("windspeed_10m")[time])
    wind_direction = _get_wind_direction(
        observation.get("winddirection_10m")[time], wind_speed
    )

    # return formatted string for activity description
    return (
        icon + " ",
        f"{condition}, {temperature}ºF, Feels like {feels_like}ºF, Humidity {humidity}%, Wind {wind_speed}mph{wind_direction}",
    )


def _get_condition_and_icon(code, is_day) -> tuple[str, str]:
    """If weather code is N/A, then returns an empty string."""

    condition, icon = "", ""

    if code == 0:
        if is_day:
            condition, icon = "Sunny", ":sun:"
        else:
            condition, icon = "Clear", ":crescent_moon:"
    elif code == 1:
        if is_day:
            condition, icon = "Mostly sunny", ":sun_behind_small_cloud:"
        else:
            condition, icon = "Mostly clear", ":crescent_moon:"
    elif code == 2:
        condition = "Partly cloudy"
        if is_day:
            icon = ":sun_behind_cloud:"
        else:
            icon = ":cloud:"
    elif code == 3:
        condition, icon = "Cloudy", ":cloud:"
    elif code in (45, 48):
        condition, icon = "Fog", ":fog:"
    elif code in (51, 53, 55):
        condition, icon = "Drizzle", ":cloud_with_rain:"
    elif code in (56, 57):
        condition, icon = "Freezing drizzle", ":cloud_with_rain:"
    elif code in (61, 63, 65):
        condition, icon = "Rain", ":cloud_with_rain:"
    elif code in (66, 67):
        condition, icon = "Freezing rain", ":cloud_with_rain:"
    elif code in (71, 73, 75, 77):
        condition, icon = "Snow", ":cloud_with_snow:"
    elif code in (80, 81, 82):
        condition = "Rain showers"
        if is_day:
            icon = ":sun_behind_rain_cloud:"
        else:
            icon = ":cloud_with_rain:"
    elif code in (85, 86):
        condition, icon = "Snow showers", ":cloud_with_snow:"
    elif code == 95:
        condition, icon = "Scattered thunderstorms", ":cloud_with_lightning_and_rain:"
    elif code in (96, 99):
        condition, icon = "Thunderstorms", ":cloud_with_lightning_and_rain:"

    return condition, emoji.emojize(icon) if icon else ""


def _get_wind_direction(angle, speed) -> str:
    """Takes an angle from 0 to 360 and returns the associated cardinal direction."""

    if speed == 0:
        return ""

    direction = " from "

    if 348.75 <= angle <= 360 or 0 <= angle < 11.25:
        direction += "N"
    elif 11.25 <= angle < 33.75:
        direction += "NNE"
    elif 33.75 <= angle < 56.25:
        direction += "NE"
    elif 56.25 <= angle < 78.75:
        direction += "ENE"
    elif 78.75 <= angle < 101.25:
        direction += "E"
    elif 101.25 <= angle < 123.75:
        direction += "ESE"
    elif 123.75 <= angle < 146.25:
        direction += "SE"
    elif 146.25 <= angle < 168.75:
        direction += "SSE"
    elif 168.75 <= angle < 191.25:
        direction += "S"
    elif 191.25 <= angle < 213.75:
        direction += "SSW"
    elif 213.75 <= angle < 236.25:
        direction += "SW"
    elif 236.25 <= angle < 258.75:
        direction += "WSW"
    elif 258.75 <= angle < 281.25:
        direction += "W"
    elif 281.25 <= angle < 303.75:
        direction += "WNW"
    elif 303.75 <= angle < 326.25:
        direction += "NW"
    elif 326.25 <= angle < 348.75:
        direction += "NNW"
    else:
        return ""

    return direction
