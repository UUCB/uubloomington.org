import pypco
from django.conf import settings
from planningcenter_events.models import Event
from site_settings.models import SiteWideSettings
from django.utils import timezone
from django.utils.dateparse import parse_datetime


def get_pco():
    pco = pypco.PCO(
        settings.PLANNING_CENTER_APPLICATION_ID,
        settings.PLANNING_CENTER_SECRET,
    )
    return pco


def get_events() -> list:
    site_settings = SiteWideSettings.load()
    pco = get_pco()
    output_events = []
    upcoming_event_instances = pco.get(
        '/calendar/v2/event_instances',
        order='starts_at',
        include='event',
        filter='future',
    )
    for event_instance in upcoming_event_instances["data"]:
        if event_instance['attributes']['all_day_event']:
            continue  # Ignore all day events for now, as we currently have no good way to display them
        if len(output_events) > site_settings.max_fetched_planning_center_events:
            break  # Break out of the loop if we have enough events
        event = pco.get(
            event_instance['relationships']['event']['links']['related']
        )
        if event['data']['attributes']['visible_in_church_center']\
                and event_instance['attributes']['published_starts_at']\
                and event_instance['attributes']['published_ends_at']:
            output_events.append(Event(
                planning_center_instance_id=event_instance['id'],
                planning_center_event_id=event['data']['id'],
                name=event_instance['attributes']['name'],
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
                link=f'https://uucb.churchcenter.com/calendar/event/{event_instance["id"]}',
                description=event['data']['attributes']['description'],
                # Add the other fields
                # Write the actual update function like we have in voting system
            ))
    return output_events


def update_events(events: list) -> None:
    for event in Event.objects.all():
        event.just_imported = False
        event.save()
    for new_event in events:
        try:
            event_object = Event.objects.get(planning_center_instance_id=new_event.planning_center_instance_id)
        except Event.DoesNotExist:
            event_object = Event(planning_center_instance_id=new_event.planning_center_instance_id)
        event_object.just_imported = True
        event_object.planning_center_event_id = new_event.planning_center_event_id
        event_object.name = new_event.name
        event_object.start_time = new_event.start_time
        event_object.end_time = new_event.end_time
        event_object.link = new_event.link
        event_object.description = new_event.description
        event_object.save()
    for event in Event.objects.filter(just_imported=False):
        event.delete()
