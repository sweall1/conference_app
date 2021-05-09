from rest_framework import serializers
from .models import Meeting, Location, User
from datetime import timedelta
from django.core.exceptions import ValidationError
from django.utils import timezone


class DateTimeFieldWihTZ(serializers.DateTimeField):
    # Class to make output of a DateTime Field timezone aware
    def to_representation(self, value):
        value = timezone.localtime(value)
        return super(DateTimeFieldWihTZ, self).to_representation(value)


class LocationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Location
        fields = '__all__'
        read_only_fields = ('manager',)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        manager = representation['manager']
        representation['manager'] = User.objects.get(pk=manager).username
        return representation

    def create(self, validated_data):
        conf = Location(
            name=validated_data['name'],
            address=validated_data['address'],
            manager=self.context['request'].user,
        )
        conf.save()
        return conf


class AddLocationSerializer(serializers.ModelSerializer):
    # Used to add location to meeting and show nested data
    class Meta:
        model = Location
        fields = '__all__'
        read_only_fields = ('manager', 'address')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        manager = representation['manager']
        representation['manager'] = User.objects.get(pk=manager).username
        return representation


class MeetingSerializer(serializers.ModelSerializer):
    participant_list = serializers.ListField(write_only=True)
    start = DateTimeFieldWihTZ(format='%Y-%m-%d %H:%M')
    end = DateTimeFieldWihTZ(format='%Y-%m-%d %H:%M')
    location = AddLocationSerializer(required=False)

    class Meta:
        model = Meeting
        fields = '__all__'
        read_only_fields = ('owner',)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        owner = representation['owner']
        representation['owner'] = User.objects.get(pk=owner).username

        if instance.participant_list:
            representation['participant_list'] = [
                user.email for user in instance.participant_list.all()]

        return representation

    def validate_participant_list(self, data):
        participants = []
        for value in data:
            try:
                user = User.objects.get(email=value)
                participants.append(user)
            except User.DoesNotExist:
                raise ValidationError({'email': 'No user with this email'})
        return participants

    def validate(self, data):
        super().validate(data)
        end = data['end']
        start = data['start']
        max_end_time = start + timedelta(hours=8)
        if start >= end:
            raise ValidationError(
                {'end_time': 'End time must occur after start time'})
        if end > max_end_time:
            raise serializers.ValidationError(
                {'end_time': 'The maximum meeting time is 8 hours'})
        return data

    def create(self, validated_data):

        calendar = Meeting.objects.create(
            owner=self.context['request'].user,
            event_name=validated_data['event_name'],
            meeting_agenda=validated_data['meeting_agenda'],
            start=validated_data['start'],
            end=validated_data['end'],
        )
        participant_list = validated_data.pop('participant_list')
        participant_list.append(self.context['request'].user)
        calendar.participant_list.set(participant_list)
        location = validated_data.pop('location', None)

        if location:
            try:
                # Check if the room is in company and assign to event
                conference = Location.objects.get(
                    name=location['name'], manager__company_id=calendar.owner.company_id)
            except Location.DoesNotExist:
                raise ValidationError(
                    {'location': 'This room doesnt exist in this company'})

            calendar.location = conference

        conference = Location.objects.get(name=location['name'])
        calendar.location = conference

        calendar.save()
        return calendar

