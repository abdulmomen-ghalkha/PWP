from habithub.models import app, db, User, Habit, Reminder, Tracking

def check():
    with app.app_context():
        print(" COUNTS::")
        print("Users:", User.query.count())
        print("Habits:", Habit.query.count())
        print("Reminders:", Reminder.query.count())
        print("Tracking logs:", Tracking.query.count())

        print("\n USERS:")
        for u in User.query.all():
            print(f"User {u.id}: {u.first_name} {u.last_name} ({u.email})")

        print("\n HABITS (with owners) ")
        for h in Habit.query.all():
            print(f"Habit {h.id}: {h.name}, user_id={h.user_id}, active={h.active}, created={h.creation_date}")

        print("\n REMINDERS:")
        for r in Reminder.query.all():
            print(f"Reminder {r.id}: habit_id={r.habit_id}, time={r.reminded_time}, created={r.creation_date}")

        print("\n TRACKING (first 10 rows) ")
        for t in Tracking.query.order_by(Tracking.log_time.desc()).limit(10).all():
            print(f"Tracking {t.id}: habit_id={t.habit_id}, log_time={t.log_time}")
        
        print("\n TRACKING COUNT PER HABIT:")
        for h in Habit.query.all():
            print(f"Habit {h.id} ({h.name}) logs:", Tracking.query.filter_by(habit_id=h.id).count())


if __name__ == "__main__":
    check()
