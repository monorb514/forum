# Generated by Django 4.1 on 2022-09-13 21:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0008_alter_replie_is_solution'),
    ]

    operations = [
        migrations.AlterField(
            model_name='replie',
            name='user',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='forum.profile'),
        ),
    ]
