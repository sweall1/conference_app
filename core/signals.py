from django.db.models.signals import post_save
from django.dispatch import receiver

from core.models import Meeting, Location


@receiver(post_save, sender=Meeting)
def add_meeting_to_company(sender, instance, created, **kwargs):
    if created:
        meeting = Meeting.objects.get(pk=instance.pk)
        meeting.owner.company.meetings.add(instance.pk)
        meeting.save()


@receiver(post_save, sender=Location)
def add_meeting_to_location(sender, instance, created, **kwargs):
    if created:
        location = Location.objects.get(pk=instance.pk)
        location.manager.company.locations.add(instance.pk)
        location.save()

