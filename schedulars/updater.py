from apscheduler.schedulers.background import BackgroundScheduler  # Importing BackgroundScheduler from APScheduler
from apscheduler.triggers.cron import CronTrigger  # Importing CronTrigger for scheduling cron jobs
from .jobs import send_overdue_emails, last_date_reminder_and_rent_finisher_aps  # Importing functions from jobs.py

# Function to start the scheduler
def start():
    # Create a scheduler instance
    scheduler = BackgroundScheduler()

    # Define triggers for each job
    over_due_email_trigger = CronTrigger(second='0', minute='0', hour='0')  # Trigger to send overdue emails daily at midnight
    last_date_reminder_and_rent_finisher_aps_trigger = CronTrigger(second='0', minute='5', hour='0')  # Trigger to send reminders and finish rents on the last date daily at 12:05 AM

    # Add jobs to the scheduler with respective triggers
    scheduler.add_job(send_overdue_emails, over_due_email_trigger)
    scheduler.add_job(last_date_reminder_and_rent_finisher_aps, last_date_reminder_and_rent_finisher_aps_trigger)

    # Start the scheduler
    scheduler.start()
