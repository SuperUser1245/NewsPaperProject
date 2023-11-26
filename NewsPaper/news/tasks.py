from celery import shared_task
import time
from datetime import datetime, timedelta
from .models import Post, Category, User, Subscriber
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import m2m_changed
from django.dispatch import receiver


@shared_task
def weekly_newsletter():
    posts = Post.objects.filter(post_time__gte=datetime.now() - timedelta(days=7))
    posts_cat = list(posts.values_list('categories', flat=True))
    users = set(Subscriber.objects.filter(category__in=posts_cat).values_list('user_id', flat=True))
    for user in users:
        subs_cat = list(Subscriber.objects.filter(user_id=user).values_list('category_id', flat=True))
        subs_posts = list(posts.filter(categories__in=subs_cat).values_list('post_title', 'id'))
        user_email = list(User.objects.filter(id=user).values_list('email', flat=True))

        html_content = render_to_string(
            'scheduler_app.html',
            {
                'subs_posts': subs_posts,
            }
        )

        send_mail(
            subject='All new posts from last Monday!',
            message='',
            html_message=html_content,
            from_email='example@gmail.com',
            recipient_list=user_email,
        )


@shared_task
def post_created():
    post = Post.objects.filter(post_time__gte=datetime.now() - timedelta(seconds=1))
    post_cat = list(post.values_list('categories', flat=True))
    users = set(Subscriber.objects.filter(category__in=post_cat).values_list('user_id', flat=True))
    for user in users:
        subs_cat = list(Subscriber.objects.filter(user_id=user).values_list('category_id', flat=True))
        subs_posts = list(post.filter(categories__in=subs_cat).values_list('post_title', 'id'))
        user_email = list(User.objects.filter(id=user).values_list('email', flat=True))

        html_content = render_to_string(
            'celery_daily_report.html',
            {
                'subs_posts': subs_posts,
            }
        )

        send_mail(
            subject='There is a new post in category you are subscribed to!',
            message='',
            html_message=html_content,
            from_email='example@gmail.com',
            recipient_list=user_email,
        )

