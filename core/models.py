from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    company = models.ForeignKey('Company', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.username


class Location(models.Model):
    manager = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Meeting(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owners')
    location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True)
    participant_list = models.ManyToManyField(User)
    event_name = models.CharField(max_length=50)
    meeting_agenda = models.TextField()
    start = models.DateTimeField()
    end = models.DateTimeField()

    def validate_dates(self):
        pass

    def save(self, *args, **kwargs):
        self.validate_dates()
        super(Meeting, self).save(*args, **kwargs)

    def __str__(self):
        return self.event_name


class Company(models.Model):
    name = models.CharField(max_length=50)
    locations = models.ManyToManyField(Location, blank=True)
    meetings = models.ManyToManyField(Meeting, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        # name on the admin page
        verbose_name_plural = 'Companies'
