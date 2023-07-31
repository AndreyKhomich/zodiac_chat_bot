import os
import redis
from celery.schedules import crontab

redis_url = os.environ.get('BROKER_URL')
redis_host = os.environ.get('BROKER_HOST')
redis_port = os.environ.get('BROKER_PORT')
redis_password = os.environ.get('BROKER_PASSWORD')

broker_url = redis_url
result_backend = redis_url
broker_connection_retry_on_startup = True

redis_client = redis.Redis(
    host=redis_host,
    port=redis_port,
    password=redis_password)

beat_schedule = {
    'add_horoscope_data_every_day': {
        'task': 'celery_app.add_horoscope_data',
        'schedule': crontab(hour='12', minute='10', day_of_week='1')
    },
    'delete_horoscope_data_every_day': {
        'task': 'celery_app.delete_horoscope_data',
        'schedule': crontab(hour='12', minute='00', day_of_week='1')
    },
    'add_love_horoscope_data_every_day': {
        'task': 'celery_app.add_love_horoscope_data',
        'schedule': crontab(hour='12', minute='10', day_of_week='1')
    },
    'delete_love_horoscope_data_every_day': {
        'task': 'celery_app.delete_love_horoscope_data',
        'schedule': crontab(hour='12', minute='00', day_of_week='1')
    },

    'add_finance_horoscope_data_every_day': {
        'task': 'celery_app.add_finance_horoscope_data',
        'schedule': crontab(hour='12', minute='10', day_of_week='1')
    },
    'delete_finance_horoscope_data_every_day': {
        'task': 'celery_app.delete_finance_horoscope_data',
        'schedule': crontab(hour='12', minute='00', day_of_week='1')
    },
}
