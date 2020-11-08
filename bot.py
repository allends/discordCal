from __future__ import print_function
import os
import discord
import datetime
from datetime import timedelta
from pytz import timezone
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from dotenv import load_dotenv

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']
emmett = 'sob00kp7sf2l7rf2cskulendto@group.calendar.google.com'
allen = '87aalj3tmll3n7qaq95ib60m0o@group.calendar.google.com'
sidhu = 'j05ajvtilvu618f16j9msce9gc@group.calendar.google.com'

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
client = discord.Client()

creds = None
if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
# If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'cred.json', SCOPES)
        creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open('token.pickle', 'wb') as token:
        pickle.dump(creds, token)

service = build('calendar', 'v3', credentials=creds)

# Call the Calendar API
now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
print('Getting the upcoming 10 events')
events_result = service.events().list(calendarId='primary', timeMin=now,
                                    maxResults=10, singleEvents=True,
                                    orderBy='startTime').execute()
events = events_result.get('items', [])

if not events:
    print('No upcoming events found.')
for event in events:
    start = event['start'].get('dateTime', event['start'].get('date'))
    print(start, event['summary'])

@client.event
async def on_ready():
    return
    

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content == '!availablenow':
        free = await people_now(message)
        for name in free:
            await message.channel.send(name)
    if message.content == '!killBot':
        await message.channel.send("can't kill me im coded different")
    if message.content == '!stop': await client.logout()


@client.event
async def people_now(message):
    output = ['These people are available: ']
    from pytz import timezone

    eastern = timezone('US/Eastern')
    now = (datetime.datetime.now(eastern)-timedelta(minutes=1)).replace(microsecond=0).isoformat()
    later = (datetime.datetime.now(eastern)+timedelta(minutes=1)).replace(microsecond=0).isoformat()

    events_result = service.events().list(calendarId=sidhu , timeMin = now, timeMax = later, maxResults=1).execute()
    if not events_result.get('items', []):
        output.append('sidhu')

    events_result = service.events().list(calendarId=allen , timeMin = now, timeMax = later, maxResults=1).execute()
    if not events_result.get('items', []):
        output.append('allen')

    events_result = service.events().list(calendarId=emmett , timeMin = now, timeMax = later, maxResults=1).execute()
    if not events_result.get('items', []):
        output.append('emmett')


    return output

client.run(TOKEN)
