import pickle

import pypco
from django.conf import settings
from django.utils.dateparse import parse_datetime
from django.utils import timezone
import datetime


def get_upcoming_events(count:int) -> bytes:
    """
    Returns upcoming `count` events from Planning Center's API, as `pickle`d `Event` objects.
    :param count:
    :return:
    """
    pco = pypco.PCO(settings.PLANNING_CENTER_APPLICATION_ID, settings.PLANNING_CENTER_SECRET)
    upcoming_event_instances = pco.get(
        '/calendar/v2/event_instances',
        order='starts_at',
        include='event',
        filter='future',
    )
    output_events = []
    for index, event_instance in enumerate(upcoming_event_instances['data'], start=0):
        event = pco.get(
            event_instance['relationships']['event']['links']['related']
        )
        if event_instance['attributes']['all_day_event']:
            continue  # Ignore all day events for now, as we currently have no good way to display them
        if event['data']['attributes']['visible_in_church_center']:
            if len(output_events) >= count:
                break
            output_events.append(Event(
                name=event['data']['attributes']['name'],
                start_time=timezone.localtime(
                    parse_datetime(
                        event_instance['attributes']['published_starts_at']
                    )
                ),
                end_time=timezone.localtime(
                    parse_datetime(
                        event_instance['attributes']['published_ends_at']
                    )
                ),
                link=f'https://uucb.churchcenter.com/calendar/event/{event_instance["id"]}'
            ))
    return pickle.dumps(output_events)


class Event():
    def __init__(self, name:str, link:str, start_time:datetime.datetime, end_time:datetime.datetime):
        self.name = name
        self.link = link
        self.start_time = start_time
        self.end_time = end_time

    def readable_times(self):
        return {
            'date': self.start_time.strftime('%A, %B %-d'),
            'start_time': self.start_time.strftime('%-I:%M %p'),
            'end_time': self.end_time.strftime('%-I:%M %p'),
        }
