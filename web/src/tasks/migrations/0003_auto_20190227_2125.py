# Generated by Django 2.1.5 on 2019-02-27 21:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0002_auto_20190226_1251'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tasks',
            name='email',
            field=models.EmailField(default=None, max_length=254, null=True),
        ),
    ]