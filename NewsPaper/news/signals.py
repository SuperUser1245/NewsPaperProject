from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import Post


@receiver(m2m_changed, sender=Post.categories.through)
def post_created(instance, action, **kwargs):
    if action == 'post_add':
        emails = User.objects.filter(subscriber__category__in=instance.categories.all()).values_list('email', flat=True)
        subject = f'New Post in {instance.categories}'

        text_content = (
            f'A new post available: {instance.post_title}\n'
            f'Link: {instance.get_absolute_url}'
        )
        html_content = (
            f'A new post available: {instance.post_title}<br>'
            f'<a href="http://127.0.0.1{instance.get_absolute_url()}">'
            f'Link</a>'
        )
        for email in emails:
            msg = EmailMultiAlternatives(subject, text_content, None, [email])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
