# Generated by Django 5.0.7 on 2024-09-07 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vege', '0006_alter_reportcard_date_of_report_card_generation'),
    ]

    operations = [
        migrations.AddField(
            model_name='receipe',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
    ]