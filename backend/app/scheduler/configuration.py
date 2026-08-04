from flask_apscheduler import APScheduler
import logging

from app.service.configuration import parcel_service
from app.config import refresh

logging.basicConfig(level=logging.INFO)

scheduler = APScheduler()

@scheduler.task('interval', id='expire_parcels_job', minutes=refresh)
def run_expire_parcels_task():
    with scheduler.app.app_context():
        try:
            count = parcel_service.expire_old_parcels()
            if count > 0:
                logging.info(f"[CRON] Success! Changed some statuses to EXPIRED for {count} parcels.")
            else:
                logging.info("[CRON] No overdue parcels.")
        except Exception as e:
            logging.error(f"[CRON] An error occurred while clearing parcels: {e}")