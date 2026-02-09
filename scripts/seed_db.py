from datetime import datetime, time, timedelta, UTC
from habithub.models import app, db, User, Habit, Reminder, Tracking

def seed():
    with app.app_context():
        db.session.query(Tracking).delete()
        db.session.query(Reminder).delete()
        db.session.query(Habit).delete()
        db.session.query(User).delete()
        db.session.commit()

        now = datetime.now(UTC)

        # demo users
        aleem = User(first_name="Aleem", last_name="Ud Din", email="aleem.uddin@example.com")
        abdul = User(first_name="Abdulmomen", last_name="Ghalkha", email="abdulmomen.ghalkha@example.com")
        atte  = User(first_name="Atte", last_name="Kiviniemi", email="atte.kiviniemi@example.com")
        hatem = User(first_name="Hatem", last_name="ElKharashy", email="hatem.elkharashy@example.com")

        db.session.add_all([aleem, abdul, atte, hatem])
        db.session.commit()

        # a small set of habits 
        habit_list = ["Gym", "Swimming", "Running", "Study", "Drink Water"]

        # create habits for each user
        users = [aleem, abdul, atte, hatem]
        for u in users:
            for hname in habit_list:
                db.session.add(Habit(
                    user_id=u.id,
                    name=hname,
                    active=True,
                    creation_date=now
                ))
        db.session.commit()

        # grab a few habits so we can attach reminders
        aleem_gym = Habit.query.filter_by(user_id=aleem.id, name="Gym").first()
        aleem_study = Habit.query.filter_by(user_id=aleem.id, name="Study").first()
        abdul_swim = Habit.query.filter_by(user_id=abdul.id, name="Swimming").first()
        atte_water = Habit.query.filter_by(user_id=atte.id, name="Drink Water").first()
        hatem_run = Habit.query.filter_by(user_id=hatem.id, name="Running").first()

        # reminders 
        db.session.add(Reminder(habit_id=aleem_gym.id, reminded_time=time(19, 0), creation_date=now))
        db.session.add(Reminder(habit_id=aleem_study.id, reminded_time=time(9, 0), creation_date=now))
        db.session.add(Reminder(habit_id=abdul_swim.id, reminded_time=time(18, 30), creation_date=now))
        db.session.add(Reminder(habit_id=atte_water.id, reminded_time=time(12, 0), creation_date=now))
        db.session.add(Reminder(habit_id=hatem_run.id, reminded_time=time(7, 30), creation_date=now))
        db.session.commit()

        # tracking logs:
        # Aleem gym: 5-day streak
        for i in range(5):
            db.session.add(Tracking(habit_id=aleem_gym.id, log_time=now - timedelta(days=i)))

        # Abdul swimming: missed one day (so it's not a perfect streak)
        db.session.add(Tracking(habit_id=abdul_swim.id, log_time=now))
        db.session.add(Tracking(habit_id=abdul_swim.id, log_time=now - timedelta(days=1)))
        db.session.add(Tracking(habit_id=abdul_swim.id, log_time=now - timedelta(days=3)))

        # Atte: small streak for water (3 days)
        for i in range(3):
            db.session.add(Tracking(habit_id=atte_water.id, log_time=now - timedelta(days=i)))

        # Hatem: only 2 logs
        db.session.add(Tracking(habit_id=hatem_run.id, log_time=now))
        db.session.add(Tracking(habit_id=hatem_run.id, log_time=now - timedelta(days=2)))

        db.session.commit()

        print("Seed done.")
        print("Users:", User.query.count())
        print("Habits:", Habit.query.count())
        print("Reminders:", Reminder.query.count())
        print("Tracking logs:", Tracking.query.count())

if __name__ == "__main__":
    seed()
