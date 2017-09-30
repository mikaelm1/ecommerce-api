from ecommerce import celery_app
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from .models import User


@celery_app.task
def send_acct_confirm_email(uid, url):
    if settings.TESTING:
        print('TESTING mode. Not sending email.')
        return
    print('Sending account confirmation email')
    user = User.objects.filter(id=uid).first()
    if user is None:
        print("Serious error. User not found")
        return
    html_content = render_to_string('email/register.html',
                                    context={'url': url, 'user': user})
    text_content = strip_tags(html_content)
    if settings.DEBUG:
        subj, sender, to = ('Account Confirmation', settings.EMAIL_HOST_USER,
                            'mikaelm1013@gmail.com')
    else:
        subj, sender, to = ('Account Confirmation', settings.EMAIL_HOST_USER,
                            user.email)
    msg = EmailMultiAlternatives(subj, text_content,
                                 sender,
                                 [to])
    msg.attach_alternative(html_content, 'text/html')
    msg.send()
