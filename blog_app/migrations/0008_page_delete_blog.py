# Generated by Django 4.2.4 on 2023-09-11 23:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog_app', '0007_alter_avatar_img_alter_avatar_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_page', models.CharField(max_length=50)),
                ('tema_page', models.CharField(max_length=50)),
                ('contenido_page', models.TextField()),
                ('fecha_page', models.DateTimeField(auto_now_add=True)),
                ('imagen_page', models.ImageField(upload_to='page_images')),
                ('autor_page', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='Blog',
        ),
    ]
