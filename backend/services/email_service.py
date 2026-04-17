import requests
from celery import shared_task
from django.conf import settings


def send_welcome_email(user_email, username):
    """Send a welcome email via external API"""
    response = requests.post(
        f'{settings.EMAIL_API_URL}/send',
        json={
            'to': user_email,
            'subject': f'Welcome {username}!',
            'body': f'Hello {username}, welcome to our platform.',
        },
        headers={'Authorization': f'Bearer {settings.EMAIL_API_KEY}'},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


@shared_task(bind=True, max_retries=3)
def send_notification_email(self, user_email, subject, body):
    """Background task to send notification emails"""
    try:
        response = requests.post(
            f'{settings.EMAIL_API_URL}/send',
            json={
                'to': user_email,
                'subject': subject,
                'body': body,
            },
            headers={'Authorization': f'Bearer {settings.EMAIL_API_KEY}'},
            timeout=30,
        )
        response.raise_for_status()
        return {'status': 'sent', 'email': user_email}
    except requests.exceptions.RequestException as exc:
        self.retry(exc=exc, countdown=60)


def fetch_user_notifications(user_id):
    """Fetch notifications from external service"""
    response = requests.get(
        f'{settings.NOTIFICATION_API_URL}/users/{user_id}/notifications',
        timeout=10,
    )
    response.raise_for_status()
    return response.json()
