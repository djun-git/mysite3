# Generated by Django 4.0.4 on 2022-05-29 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0011_timu'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timu',
            name='timu',
            field=models.CharField(max_length=1000, verbose_name='题目'),
        ),
    ]