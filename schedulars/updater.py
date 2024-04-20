from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from .jobs import send_overdue_emails, last_date_reminder_and_rent_finisher_aps

def start():
        # Create a scheduler instance
    scheduler = BackgroundScheduler()

    over_due_email_trigger = CronTrigger(second='0', minute='0', hour='0')
    scheduler.add_job(send_overdue_emails, over_due_email_trigger)

    last_date_reminder_and_rent_finisher_aps_trigger = CronTrigger(second='0', minute='5', hour='0')
    scheduler.add_job(last_date_reminder_and_rent_finisher_aps, last_date_reminder_and_rent_finisher_aps_trigger)

    # Start the scheduler
    scheduler.start()