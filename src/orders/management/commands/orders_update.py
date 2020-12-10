import datetime
from django.core.management.base import BaseCommand
from django.utils import timezone
from orders.models import Order

# command to be executed at the shell like this:
# python manage.py orders_update


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        now = timezone.now()
        today_start = now.replace(
            hour=0, minute=0, second=0, microsecond=0)
        - datetime.timedelta(days=2)
        today_end = now.replace(
            hour=23, minute=59, second=59, microsecond=999999)
        - datetime.timedelta(days=2)
        print(f"Start date: {today_start}")
        print(f"End date: {today_end}")
        qs = Order.objects.filter(
            timestamp__gte=today_start,
            timestamp__lte=today_end,
            status="created")
        qs.update(status="stale")
