# Generated by Django 5.1.4 on 2024-12-08 10:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('checkQueries', '0004_alter_query_ip_or_domain'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='scanhistory',
            name='vulnerabilities',
        ),
    ]
