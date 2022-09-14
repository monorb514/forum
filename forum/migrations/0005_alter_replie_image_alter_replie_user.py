# Generated by Django 4.1 on 2022-09-13 16:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0004_remove_replie_post_comment_post_comments'),
    ]

    operations = [
        migrations.AlterField(
            model_name='replie',
            name='image',
            field=models.ImageField(blank=True, default='', upload_to='images'),
        ),
        migrations.AlterField(
            model_name='replie',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='forum.profile'),
        ),
    ]
