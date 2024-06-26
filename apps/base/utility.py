from rest_framework.pagination import PageNumberPagination
import re
import threading
from django.core.mail import EmailMessage
from django.template.loader import render_to_string


class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self) -> None:
        self.email.send()

class Email:
    @staticmethod
    def sent_email(data):
        email = EmailMessage(
            subject=data['subject'],
            body = data['body'],
            to = [data['to_email']]
        )        
        if data.get('content_type') == "html":
            email.content_subtype = 'html'

        EmailThread(email).start()    

def sent_email(email, subject, code):
    html_content = render_to_string(
        template_name='auth/sent_email_code.html',
        context={'subject':subject, 'code' : code}
    )
    Email.sent_email(
        {
            'subject' : subject,
            'body' : html_content,
            'to_email' : email,
            'content_type' : 'html'
        }
        
    )

