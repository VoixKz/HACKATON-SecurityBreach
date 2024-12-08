from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator, RegexValidator
from authApp.models import CustomUser
from parsingVulnerabilities.models import Vulnerability, Exploit



query_status = [
    ('secured', 'Защищен'),
    ('vulnerable', 'Уязвим'),
    ('other', 'Другое')
]


class Query(models.Model):
    ip_or_domain = models.CharField(
        max_length=255,
        verbose_name="IP или домен",
        validators=[
            RegexValidator(
                regex=r'^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$|^(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}$',
                message="Введите корректный IP-адрес или домен"
            )
        ]
    )
    status = models.CharField(max_length=50, choices=query_status, verbose_name="Статус")
    vulnerabilities = models.ManyToManyField(Vulnerability, verbose_name="Уязвимости", blank=True)
    applied_exploits = models.TextField(verbose_name="Примененные эксплойты и РоС", blank=True)
    vulnerable_services_or_apps = models.TextField(verbose_name="Уязвимые сервисы или приложения", blank=True)

    def __str__(self):
        return f"{self.ip_or_domain} - {self.status}"

    class Meta:
        verbose_name = "Запрос"
        verbose_name_plural = "Запросы"

    def clean(self):
        if not self.ip_or_domain:
            raise ValidationError("IP или домен не может быть пустым")
        if self.status not in dict(query_status):
            raise ValidationError("Некорректный статус")


class ScanHistory(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="Пользователь")
    query = models.ForeignKey(Query, on_delete=models.CASCADE, verbose_name="Запрос")
    search_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата поиска")

    def __str__(self):
        return f"{self.user.email} - {self.query} - {self.search_date}"

    class Meta:
        verbose_name = "История сканирования"
        verbose_name_plural = "Истории сканирования"

    def clean(self):
        if not self.query:
            raise ValidationError("Запрос не может быть пустым")