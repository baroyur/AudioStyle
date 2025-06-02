from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator

class Poll(models.Model):
    title = models.CharField("Тема голосования", max_length=200)
    max_choices = models.PositiveIntegerField("Максимум вариантов для выбора", default=1, validators=[MinValueValidator(1)])

    def __str__(self):
        return self.title

class PollOption(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name="options")
    option_text = models.CharField("Вариант", max_length=200)

    def __str__(self):
        return self.option_text

class Vote(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    option = models.ForeignKey(PollOption, on_delete=models.CASCADE)
    ip_address = models.GenericIPAddressField("IP адрес")
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['ip_address', 'poll']),
        ]
