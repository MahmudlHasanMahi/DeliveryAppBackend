# Generated by Django 5.0.3 on 2024-03-22 17:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Webhook', '0009_alter_webhook_api_key_alter_webhook_secret_key'),
    ]

    operations = [
        migrations.AddField(
            model_name='webhook',
            name='activated',
            field=models.BooleanField(default=True),
        ),
    ]
