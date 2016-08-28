#!/usr/bin/python
from __future__ import print_function
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.template.response import TemplateResponse
from models import CalendarEvent
import simplejson
import urllib
from bson import json_util
import json
import cgi, cgitb 
import httplib2
import os
import datetime
from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools
from django.conf import settings

try:
    import argparse
    flags = tools.argparser.parse_args([])
except ImportError:
    flags = None

cgitb.enable()  # for troubleshooting

def index(request):
    events = CalendarEvent.objects.values('title','start', 'end', 'id')
    ev = JsonResponse(list(events), safe=False)
    return TemplateResponse(request, 'home/index.html', {'event_l':ev.content},)

@csrf_exempt        
def post_events_data(request):
    if request.method == 'POST' and request.is_ajax():
        data_string = request.POST.get('json_data')
        data_dict = json.loads(data_string)
        title_data=data_dict['title']
        start_data=data_dict['start']
        end_data=data_dict['end']
        p = CalendarEvent(title=title_data, start=start_data, end=end_data, all_day=1)
        p.save()
        return index(request)
        
@csrf_exempt
def modify_events_data(request):
    if request.method == 'POST' and request.is_ajax():
        data_string = request.POST.get('json_data')
        data_dict = json.loads(data_string)
        title_data=data_dict['title']
        start_data=data_dict['start']
        end_data=data_dict['end']
        eid=data_dict['eid']
        evnt = CalendarEvent.objects.get(pk = eid)
        evnt.title=title_data
        evnt.start=start_data
        evnt.end=end_data
        evnt.save()
        return index(request)
        
@csrf_exempt
def delete_events_data(request):
   if request.method == 'POST' and request.is_ajax():
       data_string = request.POST.get('json_data')
       data_dict = json.loads(data_string)
       eid=data_dict['id']
       evnt = CalendarEvent.objects.get(pk = eid)
       evnt.delete()
       return index(request)

SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SECRET_FILE = os.path.join(settings.PROJECT_ROOT, 'client_secret.json')
APPLICATION_NAME = 'Google Calendar API Python Quickstart'

@csrf_exempt
def get_credentials():
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'calendar-python-quickstart.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

@csrf_exempt
def google_calendar_sync(request):
    #print("Breakpoint --> google_calendar_sync")
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    #print('Getting the upcoming 10 events')
    eventsResult = service.events().list(
        calendarId='primary', timeMin=now, maxResults=10, singleEvents=True,
        orderBy='startTime').execute()
    events = eventsResult.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        end = event['start'].get('dateTime', event['end'].get('date'))
        #print(start, end, event['summary'])
        title_data=event['summary']
        start_data=start
        end_data=end
        p = CalendarEvent(title=title_data, start=start_data, end=end_data, all_day=1)
        p.save()
    return index(request)
