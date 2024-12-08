from django.db import models
from authApp.models import CustomUser
from django.core.validators import URLValidator

class Vulnerability(models.Model):
    vulnerability_id = models.CharField(
        max_length=500,
        unique=True,
        verbose_name="ID уязвимости",
        blank=True
    )
    description = models.TextField(verbose_name="Описание")
    publication_date = models.DateField(verbose_name="Дата публикации")
    exploits = models.ManyToManyField('Exploit', related_name='related_vulnerabilities', verbose_name="Эксплойты")

    def __str__(self):
        return self.vulnerability_id

    class Meta:
        verbose_name = "Уязвимость"
        verbose_name_plural = "Уязвимости"


class Exploit(models.Model):
    exploit_id = models.CharField(
        max_length=500,
        unique=True,
        verbose_name="ID эксплойта"
    )
    name = models.CharField(max_length=500, verbose_name="Название")
    publication_date = models.DateField(verbose_name="Дата публикации эксплойта")
    description = models.TextField(verbose_name="Описание эксплойта")
    repository_url = models.URLField(validators=[URLValidator()], verbose_name="URL репозитория")
    entrypoint = models.CharField(max_length=255, verbose_name="Точка входа скрипта")
    args = models.TextField(verbose_name="Дополнительные аргументы")
    vulnerabilities = models.ManyToManyField(Vulnerability, related_name='related_exploits', verbose_name="Уязвимости")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Эксплойт"
        verbose_name_plural = "Эксплойты"