# Generated by Django 2.2 on 2021-02-20 21:17

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='email',
            field=models.EmailField(default=datetime.datetime(2021, 2, 20, 21, 16, 53, 473072, tzinfo=utc), max_length=254),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='password',
            field=models.CharField(default='aaaa', max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='transaction',
            name='trans_type',
            field=models.CharField(choices=[('Deposit', 'deposit'), ('Withdrawal', 'withdrawal'), ('Savings', 'savings'), ('Transfer', 'transfer')], max_length=30),
        ),
    ]
