# Generated by Django 2.0.6 on 2018-06-05 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parser', '0002_auto_20180605_1630'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courses',
            name='id',
            field=models.CharField(default=None, max_length=15, primary_key=True, serialize=False),
        ),
    ]
