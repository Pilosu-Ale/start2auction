# Generated by Django 3.2.6 on 2021-10-04 13:32

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('api_auction', '0005_alter_auction_start_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction',
            name='end_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 4, 13, 35, 23, 798186, tzinfo=utc)),
        ),
    ]
