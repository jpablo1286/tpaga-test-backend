# Generated by Django 2.1.4 on 2018-12-22 22:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('miniapp', '0002_auto_20181222_1816'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='cost',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
