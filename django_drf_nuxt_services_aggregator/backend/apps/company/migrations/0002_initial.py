# Generated by Django 4.0.5 on 2022-06-15 10:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('city', '0001_initial'),
        ('company', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='point',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Автор'),
        ),
        migrations.AddField(
            model_name='point',
            name='city',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='city.city', verbose_name='Город'),
        ),
        migrations.AddField(
            model_name='point',
            name='metro',
            field=models.ManyToManyField(blank=True, to='city.metrostation', verbose_name='Станции метро'),
        ),
        migrations.AddField(
            model_name='companyimage',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='company.company', verbose_name='Компания'),
        ),
        migrations.AddField(
            model_name='company',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Автор'),
        ),
        migrations.AddField(
            model_name='company',
            name='brands',
            field=models.ManyToManyField(blank=True, to='company.brand', verbose_name='Бренды'),
        ),
        migrations.AddField(
            model_name='company',
            name='categories',
            field=models.ManyToManyField(blank=True, related_name='companies', to='company.category', verbose_name='Категории'),
        ),
        migrations.AddField(
            model_name='company',
            name='city',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='city.city', verbose_name='Город'),
        ),
        migrations.AddField(
            model_name='company',
            name='often_repair',
            field=models.ManyToManyField(blank=True, to='company.oftenrepair', verbose_name='Часто ремонтируем'),
        ),
        migrations.AddField(
            model_name='company',
            name='points',
            field=models.ManyToManyField(blank=True, related_name='company', to='company.point', verbose_name='Мастерские'),
        ),
        migrations.AddField(
            model_name='category',
            name='parent_category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children_category', to='company.category', verbose_name='Родительская категория'),
        ),
        migrations.AddField(
            model_name='brand',
            name='categories',
            field=models.ManyToManyField(blank=True, related_name='brands', to='company.category', verbose_name='Категории'),
        ),
    ]