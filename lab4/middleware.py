from django.utils.deprecation import MiddlewareMixin
from .models import Page, VisitorIP, Visit
from django.utils import timezone
from datetime import timedelta


class VisitCounterMiddleware(MiddlewareMixin):
    RESET_IP_AFTER = timedelta(hours=1)  # время сброса IP

    def process_request(self, request):
        # Получаем IP
        ip = self.get_client_ip(request)
        if not ip:
            return  # не можем получить IP — пропускаем

        # Получаем url страницы
        url_path = request.path

        # Получаем или создаём страницу
        page, _ = Page.objects.get_or_create(url=url_path)

        now = timezone.now()

        # Проверяем IP
        visitor_ip, created = VisitorIP.objects.get_or_create(ip_address=ip)

        # Сброс ip если время последнего визита старше лимита
        if not created and now - visitor_ip.last_visit > self.RESET_IP_AFTER:
            # Можно удалить старую запись или обновить last_visit
            visitor_ip.last_visit = now
            visitor_ip.save()
        else:
            # Обновляем время последнего визита
            visitor_ip.last_visit = now
            visitor_ip.save()

        # Увеличиваем счётчик посещений страницы
        page.visits_count = page.visits_count + 1
        page.save()

        # Создаём запись посещения
        Visit.objects.create(page=page, visitor_ip=visitor_ip, visit_time=now)

    def get_client_ip(self, request):
        # Получаем IP из заголовков
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
