As personal preference used signals.py instead of uuid field.

DEBUG = True

SECRET_KEY = os.environ.get('SECRET_KEY')

1. Create super user;
2. Create users and companies from django admin panel;
3. On the main page there is an option to log in;


At http://127.0.0.1:8000/location/ create a query f.e:
```
    {
        "name": "First",
        "address": "Gdansk"
    }
```
At http://127.0.0.1:8000/calendar/ create a query f.e:
```
 {
        "start": "2021-05-08T12:58:34Z",
        "end": "2021-05-08T13:58:33Z",
        "location": {
            "name": "First"
        },
        "event_name": "event",
        "meeting_agenda": "agenda",
        "participant_list": [
            "wp@wp.pl"
        ]
    }
```
This app covers all business reqirements listed in instruction.

1. User who creates a location is always a manager of this room;
2. User Who creates a meeting is always an owner of that meeting;
3. Meetings are visible only for those users who are from the same company and have an invitation or are manager of the conference room;
4. Meetings can't last longer than 8 hours;
5. Datetime fields are visible in currently logged user local timezone;

Additionally:
1. End meeting time must occur after start time;
2. User who creates a meeting is added to participant_list;
3. Check if user email exits while creating a meeting;
4. Check if conference room exits in users company while creating a meeting;


Filters:

1. Events in specifing conference room

http://127.0.0.1:8000/calendar/?location=6

2. Agenda/event_name name filter:

http://127.0.0.1:8000/calendar/?search=foo+bar

3. Day filter

http://127.0.0.1:8000/calendar/?day=2021-05-09
