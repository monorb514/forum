# Generated by Django 4.1 on 2022-09-13 13:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='visit_count',
            field=models.IntegerField(default=0),
        ),
    ]
