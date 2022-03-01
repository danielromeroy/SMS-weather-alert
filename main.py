import requests as rq
from twilio.rest import Client
import os

# Malaga
# LAT = 36.598642
# LON = -4.561405

sending_sms = False

# Copenhagen
LAT = 55.817941
LON = 12.531953

account_sid = os.environ["TWILIO_SID"]
auth_token = os.environ["TWILIO_AUTH_TOKEN"]
client = Client(account_sid, auth_token)


def send_notification():
    print("Raining in the next few hours. Sending SMS message...")
    message = "It's going to rain today. Remember to take an ☔."
    if sending_sms:
        message = client.messages.create(body=message,
                                         from_='+12764008929',
                                         to='+34659799897')
        print(message.status)
    else:
        print(f"Not sendig SMS. Printing message instead:\n\n{message}")


openweathermap_api_key = os.environ["OPENWEATHERMAP_API_KEY"]
one_call_api = "https://api.openweathermap.org/data/2.5/onecall"

params = {
    "lat": LAT,
    "lon": LON,
    "appid": openweathermap_api_key,
    "exclude": "minutely,current,daily"
}

response = rq.get(one_call_api, params)
response.raise_for_status()
data = response.json()

ids = [data["hourly"][i]["weather"][0]["id"] for i in range(12)]

if any(weather_id < 800 for weather_id in ids):
    send_notification()
else:
    print("No rain in the next 12 hours.")
