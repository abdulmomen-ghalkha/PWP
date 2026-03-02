"""Defines converters needed by habithubt"""

from werkzeug.routing import BaseConverter
from werkzeug.exceptions import NotFound
from . import db
from .models import User, Habit, Reminder, Tracking

class UserConverter(BaseConverter):
    """Converter for user type"""
    def to_python(self, user_id):
        """Converts a uri to a user object"""
        user = db.session.get(User, user_id)
        if user is None:
            raise NotFound
        return user

    def to_url(self, user):
        """Converts a user object to uri by using id"""
        return str(user.id)


class HabitConverter(BaseConverter):
    """Converter for habit type"""
    def to_python(self, habit_id):
        """Converts a uri to a habit object"""
        habit = db.session.get(Habit, habit_id)
        if habit is None:
            raise NotFound
        return habit

    def to_url(self, habit):
        """Converts a habit object to uri by using id"""
        return str(habit.id)


class ReminderConverter(BaseConverter):
    """Converter for reminder type"""
    def to_python(self, reminder_id):
        """Converts a uri to a reminder object"""
        reminder = db.session.get(Reminder, reminder_id)
        if reminder is None:
            raise NotFound
        return reminder

    def to_url(self, reminder):
        """Converts a reminder object to uri by using id"""
        return str(reminder.id)


class TrackingConverter(BaseConverter):
    """Converter for tracking type"""
    def to_python(self, tracking_id):
        """Converts a uri to a tracking object"""
        tracking = db.session.get(Tracking, tracking_id)
        if tracking is None:
            raise NotFound
        return tracking

    def to_url(self, tracking):
        """Converts a tracking object to uri by using id"""
        return str(tracking.id)
