from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

def send_match_notification_email(user, other_profile):
    """Notify user that they have a new match"""
    subject = f"You matched with {other_profile.display_name}!"
    
    context = {
        'user': user,
        'other': other_profile,
        'site_name': 'DatingApp'
    }
    
    html_message = render_to_string('emails/match_notification.html', context)
    plain_message = f"Hi! You have a new match with {other_profile.display_name} on DatingApp. Check your inbox to start chatting!"
    
    send_mail(
        subject,
        plain_message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        html_message=html_message,
        fail_silently=True
    )
