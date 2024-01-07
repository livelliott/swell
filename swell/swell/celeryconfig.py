
from datetime import timedelta

CELERY_BROKER_URL = 'redis://localhost:6379/0'  # Replace with your broker URL
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'  # Replace with your backend URL

CELERY_BEAT_SCHEDULE = {
    'send-envelopes': {
        'task': 'board.tasks.schedule_send_envelope_email',
        'schedule': timedelta(days=1),
    },
}