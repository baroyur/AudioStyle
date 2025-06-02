from django.db import models
from django.utils import timezone
from datetime import timedelta

class Page(models.Model):
    url = models.CharField(max_length=255, unique=True)
    visits_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.url


class VisitorIP(models.Model):
    ip_address = models.GenericIPAddressField(unique=True)
    last_visit = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.ip_address


class Visit(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE)
    visitor_ip = models.ForeignKey(VisitorIP, on_delete=models.CASCADE)
    visit_time = models.DateTimeField(auto_now_add=True)
