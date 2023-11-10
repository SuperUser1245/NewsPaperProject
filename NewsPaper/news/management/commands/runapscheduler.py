import logging
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.conf import settings
from django.core.management.base import BaseCommand
from django_apscheduler import util
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from news.models import Post, Category, User, Subscriber
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string

logger = logging.getLogger(__name__)


def my_job():
    posts = Post.objects.filter(post_time__gte='2023-11-17 16:30:42.347581')
    posts_cat = list(posts.values_list('categories', flat=True))
    users = set(Subscriber.objects.filter(category__in=posts_cat).values_list('user_id', flat=True))
    for user in users:
        subs_cat = list(Subscriber.objects.filter(user_id=user).values_list('category_id', flat=True))
        subs_posts = list(posts.filter(categories__in=subs_cat).values_list('post_title', 'id'))
        user_email = list(User.objects.filter(id=user).values_list('email', flat=True))
        print(subs_posts)

        html_content = render_to_string(
            'scheduler_app.html',
            {
                'subs_posts': subs_posts,
            }
        )

        send_mail(
            subject='All new posts from last Friday!',
            message='',
            html_message=html_content,
            from_email='example@gmail.com',
            recipient_list=user_email,
        )


@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    """
    This job deletes APScheduler job execution entries older than `max_age`
    from the database.
    It helps to prevent the database from filling up with old historical
    records that are no longer useful.

    :param max_age: The maximum length of time to retain historical
                    job execution records. Defaults to 7 days.
    """
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            my_job,
            trigger=CronTrigger(day_of_week='fri', minute="00", hour="18"),
            id="my_job",  # The `id` assigned to each job MUST be unique
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added weekly job: 'delete_old_job_executions'.")

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")