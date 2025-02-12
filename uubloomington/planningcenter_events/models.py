from django.db import models
from modelcluster.models import ClusterableModel
from wagtail.models import Orderable


# Create your models here.
class Event(models.Model):
    planning_center_instance_id = models.IntegerField(
        primary_key=True,
        unique=True,
    )
    planning_center_event_id = models.IntegerField()
    just_imported = models.BooleanField(default=True)
    name = models.CharField(max_length=255)
    link = models.URLField(max_length=255)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    description = models.TextField(null=True, blank=True)

    def readable_times(self):
        return {
            'date': self.start_time.strftime('%A, %B %-d'),
            'start_time': self.start_time.strftime('%-I:%M %p'),
            'end_time': self.end_time.strftime('%-I:%M %p'),
        }

    def __str__(self):
        return self.name


class EventListing(ClusterableModel):
    name = models.CharField(max_length=255)
    description_must_contain = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text="Only show events which contain this text in their description. Leave blank to show all events."
    )
    show_next_events = models.IntegerField(
        default=15,
        null=False,
        blank=False,
        help_text="Show this number of events which match the filter."
    )

    def __str__(self):
        return self.name

    def get_events(self):
        if self.description_must_contain:
            return Event.objects.filter(description__contains=self.description_must_contain)[:self.show_next_events]
        else:
            return Event.objects.all()[:self.show_next_events]
