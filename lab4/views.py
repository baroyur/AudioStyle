from django.shortcuts import render
from django.utils import timezone
from datetime import timedelta
from django.db import models

from .models import Page, Visit, VisitorIP

def report(request):
    period = request.GET.get('period', 'day')

    now = timezone.now()
    if period == 'hour':
        start_time = now - timedelta(hours=1)
    elif period == 'week':
        start_time = now - timedelta(days=7)
    else:
        # по умолчанию день
        start_time = now - timedelta(days=1)

    # Страницы с ненулевыми посещениями в период
    visits = Visit.objects.filter(visit_time__gte=start_time)

    # Считаем посещения по страницам
    page_visits = visits.values('page__url').annotate(count=models.Count('id')).order_by('-count')

    # Уникальные посетители в период
    unique_ips = visits.values('visitor_ip').distinct().count()

    context = {
        'page_visits': page_visits,
        'unique_visitors': unique_ips,
        'selected_period': period,
    }
    return render(request, 'lab4/report.html', context)
