# Generated by Django 4.2.2 on 2023-06-27 02:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_inactiveitems_final_price'),
    ]

    operations = [
        migrations.CreateModel(
            name='WatchList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auctions.items')),
                ('User', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='WatchList', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
