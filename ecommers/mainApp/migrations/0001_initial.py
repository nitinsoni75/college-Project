# Generated by Django 4.0.6 on 2022-07-23 17:45

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('phone', models.CharField(max_length=10)),
                ('status', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('country', models.CharField(blank=True, max_length=20, null=True)),
                ('state', models.CharField(blank=True, default=None, max_length=20, null=True)),
                ('city', models.CharField(blank=True, default=None, max_length=20, null=True)),
                ('landmark', models.CharField(blank=True, default=None, max_length=30, null=True)),
                ('road', models.CharField(blank=True, default=None, max_length=50, null=True)),
                ('place', models.CharField(blank=True, default=None, max_length=50, null=True)),
                ('pin', models.IntegerField(blank=True, default=None, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=50)),
                ('product_title', models.TextField(max_length=300)),
                ('category', models.CharField(choices=[('Electronics', 'Electroincs'), ('Vegitables', 'Vegitables'), ('Womens Clouthes', 'Women Clouthes'), ('Mens Clouthes', 'Mens Clouthes'), ('Toys', 'Toys')], max_length=20)),
                ('quantity_type', models.CharField(choices=[('/Piece', '/Piece'), ('/kg', '/kg'), ('/Packet', '/Packet')], max_length=20)),
                ('price', models.BigIntegerField()),
                ('offer', models.IntegerField()),
                ('pro_images', models.ImageField(max_length=500, upload_to='pro_images')),
                ('total', models.IntegerField()),
                ('avaliable', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('price', models.IntegerField()),
                ('total_price', models.FloatField()),
                ('order_date', models.DateField(default=datetime.date(2022, 7, 23))),
                ('order_time', models.TimeField(default=datetime.datetime(2022, 7, 23, 23, 15, 17, 476022))),
                ('status', models.BooleanField(default=False)),
                ('order_address', models.TextField(max_length=100)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainApp.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]