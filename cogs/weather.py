from datetime import datetime

import discord
import requests
from discord.ext import commands
from pyiqvia import Client

import settings


class WeatherCog(commands.Cog):
    """Return weather information.

    This cog is used to provide allergen and general
    weather information using the OpenWeatherMap and Ambee APIs.

    The `ctx` argument is treated as `self` for commands and is omitted from documentation.
    """

    api_openweather = "&appid={api_key}".format(api_key=settings.OPENWEATHERMAP_API_KEY)
    api_ambee = ""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def forecast(self, ctx, location: str, days: int = 1):
        """Returns the forecast for `n` days.

        Create a series of forecast objects for a number of days.
        This supports location lookup using city/state, zip code, lat/long.

        Parameters:
            location (str): Location information in quotations ("").
                            Zip codes require country abbrevation.
            days (int): Default to 1 day, the forecast for tomorrow.
        Returns:
            embed (class Embed): A message with location, datetime, weather description,
                                current temperature, feels like, humidity, temp min.,
                                temp max, wind speed, sunrise/sunset time, timezone.
        TODO:
            * Fix UTC timestamp conversion to display proper, localized time.
            * Return 1 forecast object per day, not 8 (every 3 hours).
        """
        forecast = "http://api.openweathermap.org/data/2.5/forecast?q={location}&units=imperial".format(
            location=location
        )
        forecast += WeatherCog.api_openweather
        api_call = requests.get(forecast)
        weather = WeatherCog._format_forecast_data(api_call.json())

        for x in range(days):
            await ctx.send(embed=weather[x])

    @commands.command()
    async def weather_now(self, ctx, location: str):
        """Returns the current weather.

        Create an embed object with the current weather for a location.
        This supports location lookup using city/state, zip code, lat/long.

        Parameters:
            location (str): Location information in quotations ("").
                            Zip codes require country abbrevation.
        Returns:
            embed (class Embed): A message with location, datetime, weather description,
                                current temperature, feels like, humidity, temp min.,
                                temp max, wind speed, sunrise/sunset time, timezone.
        TODO:
            * Fix UTC timestamp conversion to display proper, localized time.
        """
        forecast = "http://api.openweathermap.org/data/2.5/weather?q={location}&units=imperial".format(
            location=location
        )
        forecast += WeatherCog.api_openweather
        api_call = requests.get(forecast)
        weather = WeatherCog._format_weather_data(api_call.json())

        await ctx.send(embed=weather)

    @commands.command()
    async def pollen(self, ctx, zip_code: str):
        """3 day pollen index.

        Pulls a 3 day pollen index with allergen information from `pollen.com`
        using the `pyiqvia` wrapper.

        Parameters:
            zip_code (str): Converted to string for convenience with piqvia.
        Returns:
            message (class Embed): The pollen index and allergen information
                                (allergen name, genus, and plant type) for the day.
        """
        client = Client(zip_code)
        data = await client.allergens.current()
        allergens = WeatherCog._format_pollen_data(data)

        await ctx.send(embed=allergens)

    @staticmethod
    def _lat_lang(location: str):
        forecast = "http://api.openweathermap.org/data/2.5/weather?q={location}&units=imperial".format(
            location=location
        )
        forecast += WeatherCog.api_openweather
        api_call = requests.get(forecast)
        weather = api_call.json()
        coords = {
            "latitude": weather["coord"]["lat"],
            "longitude": weather["coord"]["lon"],
        }
        return coords

    @staticmethod
    def _format_forecast_data(data):
        weather = []
        for x in data["list"]:
            weather.append(
                {
                    "date": datetime.utcfromtimestamp(x["dt"]).strftime(
                        "%m-%d-%Y %I:%M %p"
                    ),
                    "current_temp": x["main"]["temp"],
                    "feels_like": x["main"]["feels_like"],
                    "temp_min": x["main"]["temp_min"],
                    "temp_max": x["main"]["temp_max"],
                    "humidity": x["main"]["humidity"],
                    "weather": x["weather"][0]["main"],
                    "weather_desc": x["weather"][0]["description"],
                    "wind": x["wind"]["speed"],
                }
            )
        city = {
            "name": data["city"]["name"],
            "country": data["city"]["country"],
            "sunrise": datetime.utcfromtimestamp(data["city"]["sunrise"]).strftime(
                "%m-%d-%Y %I:%M %p"
            ),
            "sunset": datetime.utcfromtimestamp(data["city"]["sunset"]).strftime(
                "%m-%d-%Y %I:%M %p"
            ),
            "timezone": data["city"]["timezone"],
            "latitude": data["city"]["coord"]["lat"],
            "longitude": data["city"]["coord"]["lon"],
        }
        desc = f'**{city["name"]}, {city["country"]}**\n'.format(city=city)
        embeds = []
        for x in weather:
            embed = discord.Embed(
                title="Weather data for: " + x["date"], color=0x27E1DC
            )
            embed.set_author(
                name="BrandoBot#9684", url="https://github.com/mattdood/brandobot"
            )
            embed.description = desc + x["weather"] + " with " + x["weather_desc"]
            embed.add_field(name="Current Temp", value=x["current_temp"], inline=True)
            embed.add_field(name="Feels Like", value=x["feels_like"], inline=True)
            embed.add_field(name="Humidity", value=x["humidity"], inline=True)
            embed.add_field(name="Temp Min", value=x["temp_min"], inline=True)
            embed.add_field(name="Temp Max", value=x["temp_max"], inline=True)
            embed.add_field(name="Wind Speed", value=x["wind"], inline=True)
            embed.add_field(name="Sunrise", value=city["sunrise"], inline=True)
            embed.add_field(name="Sunset", value=city["sunset"], inline=True)
            embed.add_field(name="Timezone", value=city["timezone"], inline=True)
            embed.set_footer(
                text=f"Use `!pm_more_comments <comment_id>` to read more!  |  {datetime.now()}"
            )
            embeds.append(embed)
        return embeds

    @staticmethod
    def _format_weather_data(data):
        weather = {
            "date": datetime.utcfromtimestamp(data["dt"]).strftime("%m-%d-%Y %I:%M %p"),
            "current_temp": data["main"]["temp"],
            "feels_like": data["main"]["feels_like"],
            "temp_min": data["main"]["temp_min"],
            "temp_max": data["main"]["temp_max"],
            "humidity": data["main"]["humidity"],
            "weather": data["weather"][0]["main"],
            "weather_desc": data["weather"][0]["description"],
            "wind": data["wind"]["speed"],
        }
        city = {
            "name": data["name"],
            "country": data["sys"]["country"],
            "sunrise": datetime.utcfromtimestamp(data["sys"]["sunrise"]).strftime(
                "%m-%d-%Y %I:%M %p"
            ),
            "sunset": datetime.utcfromtimestamp(data["sys"]["sunset"]).strftime(
                "%m-%d-%Y %I:%M %p"
            ),
            "timezone": data["timezone"],
            "latitude": data["coord"]["lat"],
            "longitude": data["coord"]["lon"],
        }
        desc = f'**{city["name"]}, {city["country"]}**\n'.format(city=city)

        embed = discord.Embed(
            title="Weather data for: " + weather["date"], color=0x27E1DC
        )
        embed.set_author(
            name="BrandoBot#9684", url="https://github.com/mattdood/brandobot"
        )
        embed.description = (
            desc + weather["weather"] + " with " + weather["weather_desc"]
        )
        embed.add_field(name="Current Temp", value=weather["current_temp"], inline=True)
        embed.add_field(name="Feels Like", value=weather["feels_like"], inline=True)
        embed.add_field(name="Humidity", value=weather["humidity"], inline=True)
        embed.add_field(name="Temp Min", value=weather["temp_min"], inline=True)
        embed.add_field(name="Temp Max", value=weather["temp_max"], inline=True)
        embed.add_field(name="Wind Speed", value=weather["wind"], inline=True)
        embed.add_field(name="Sunrise", value=city["sunrise"], inline=True)
        embed.add_field(name="Sunset", value=city["sunset"], inline=True)
        embed.add_field(name="Timezone", value=city["timezone"], inline=True)
        embed.set_footer(
            text=f"Use `!pm_more_comments <comment_id>` to read more!  |  {datetime.now()}"
        )
        return embed

    @staticmethod
    def _format_pollen_data(data):
        info = {
            "date": datetime.now().strftime("%m-%d-%Y"),
            "city": data["Location"]["DisplayLocation"],
        }
        days = []
        for x in data["Location"]["periods"]:
            days.append(x)

        desc = f'**{info["city"]}**\n'.format(info=info)

        embed = discord.Embed(title="Pollen data for: " + info["date"], color=0x9CCC9C)
        embed.set_author(
            name="BrandoBot#9684", url="https://github.com/mattdood/brandobot"
        )
        embed.description = desc + "Pollen forecast from <https://pollen.com/>."
        for x in days:
            embed.add_field(name="Day", value=x["Type"], inline=True)
            embed.add_field(name="Index", value=x["Index"], inline=True)
            allergens = []
            for y in x["Triggers"]:
                allergen = f"Name: {y['Name']}\n\tGenus: {y['Genus']}\n\tPlant Type: {y['PlantType']}\n\n"
                allergens.append(allergen)
            allergens = "```" + "".join(allergens) + "```"
            embed.add_field(name="Allergens", value=allergens, inline=False)
            # embed.add_field(name="Name", value=y["Name"])
            # embed.add_field(name="Genus", value=y["Genus"])
            # embed.add_field(name="Plant Type", value=y["PlantType"])
        embed.set_footer(
            text=f"Use `!help weathercog` to see more!  |  {datetime.now()}"
        )
        return embed
