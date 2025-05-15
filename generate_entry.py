import datetime
import requests
import click

# Example usage:
# python3 generate_entry.py "Two globular clusters" "Mediocre seeing."
# Optional: --lat 51.0 --lon 4.7 to override location


DEFAULT_LAT = 50.9502
DEFAULT_LON = 4.7115

API_TEMPLATE = (
    "https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}"
    "&current=temperature_2m,cloudcover,wind_speed_10m,wind_direction_10m"
)

def get_weather_summary(lat, lon):
    url = API_TEMPLATE.format(lat=lat, lon=lon)
    res = requests.get(url)
    data = res.json()['current']
    temp = data['temperature_2m']
    cloud = data['cloudcover']
    wind_speed = data['wind_speed_10m']
    wind_dir = data['wind_direction_10m']

    cloud_desc = (
        "clear" if cloud < 20 else
        "partly cloudy" if cloud < 50 else
        "mostly cloudy" if cloud < 80 else
        "overcast"
    )
    wind_desc = (
        "calm" if wind_speed < 5 else
        "light breeze" if wind_speed < 15 else
        "moderate wind"
    )

    return (
        f"Temperature: {temp}°C, Cloud cover: {cloud}%, "
        f"{cloud_desc}, Wind: {wind_speed} km/h from {wind_dir}°, {wind_desc}"
    )

def create_post(title, notes, lat, lon, date):
    filename = f"_posts/{date}-{title.replace(' ', '-')}.md"
    weather = get_weather_summary(lat, lon)

    content = f"""---
layout: post
title: {title}
date: {date}
---

**Weather:** {weather}

**Notes:**

{notes}
"""
    with open(filename, 'w') as f:
        f.write(content)
    print(f"Entry created: {filename}")

def parse_date(date_str):
    try:
        return datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        raise click.BadParameter("Date must be in YYYY-MM-DD format.")


@click.command()
@click.option('--title', '-t', default="*")
@click.option('--notes', '-n', default="TBD")
@click.option('--lat', default=DEFAULT_LAT, show_default=True, help='Latitude')
@click.option('--lon', default=DEFAULT_LON, show_default=True, help='Longitude')
@click.option('--date', default=lambda: datetime.date.today().isoformat(), show_default='today', help='Date in YYYY-MM-DD format')
def main(title, notes, lat, lon, date):
    """Create a new astronomy log entry with TITLE and NOTES."""
    date_obj = parse_date(date)
    create_post(title, notes, lat, lon, date_obj)

if __name__ == "__main__":
    main()
