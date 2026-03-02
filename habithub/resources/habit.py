"""Defines resources needed to access habit data """

from flask import Response, request, url_for
from flask_restful import Resource
from jsonschema import ValidationError, validate
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import BadRequest, Conflict, NotFound, UnsupportedMediaType
from habithub import db, cache
from habithub.models import Habit
from habithub.auth import require_api_key


def _check_habit_owner(user, habit):
    """Helper function to check the habit owner"""
    if habit.user_id != user.id:
        raise NotFound


class HabitItem(Resource):
    """Resource for managing a single habit."""

    @require_api_key
    @cache.cached()
    def get(self, user, habit):
        """GET request"""
        _check_habit_owner(user, habit)
        return habit.serialize()

    @require_api_key
    def put(self, user, habit):
        """PUT request"""
        _check_habit_owner(user, habit)
        if not request.json:
            raise UnsupportedMediaType
        try:
            validate(request.json, Habit.json_schema())
        except ValidationError as e:
            raise BadRequest(description=str(e)) from e

        habit.deserialize(request.json)
        try:
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            raise Conflict(description="Habit could not be updated") from e

        self._clear_cache(user)
        return Response(status=204)

    @require_api_key
    def delete(self, user, habit):
        """DELETE request"""
        _check_habit_owner(user, habit)
        self._clear_cache(user)
        db.session.delete(habit)
        db.session.commit()
        return Response(status=204)

    def _clear_cache(self, user):
        """Clear cached data for this habit item and the habit collection."""
        cache.delete_many(
            "view/" + request.path,
            "view/" + url_for("api.habitcollection", user=user),
        )


class HabitCollection(Resource):
    """Resource for managing the collection of habits for a user."""

    @require_api_key
    @cache.cached()
    def get(self, user):
        """GET request"""
        habits = Habit.query.filter_by(user_id=user.id).all()
        return [habit.serialize() for habit in habits]

    @require_api_key
    def post(self, user):
        """POST request"""
        if not request.json:
            raise UnsupportedMediaType
        try:
            validate(request.json, Habit.json_schema())
        except ValidationError as e:
            raise BadRequest(description=str(e)) from e

        habit = Habit(user_id=user.id)
        habit.deserialize(request.json)
        try:
            db.session.add(habit)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            raise Conflict(description="Habit could not be created") from e

        location = url_for("api.habititem", user=user, habit=habit)
        cache.delete("view/" + url_for("api.habitcollection", user=user))
        return Response(status=201, headers={"Location": location})
