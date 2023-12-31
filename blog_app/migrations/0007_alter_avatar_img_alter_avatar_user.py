# Generated by Django 4.2.4 on 2023-09-11 19:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog_app', '0006_rename_image_avatar_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='avatar',
            name='img',
            field=models.ImageField(upload_to='avatars'),
        ),
        migrations.AlterField(
            model_name='avatar',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
