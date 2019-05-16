# Generated by Django 2.2 on 2019-05-09 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0006_auto_20190509_2119'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='status',
            field=models.IntegerField(choices=[(1, 'General'), (2, 'Article'), (3, 'Guidelines')], default=1, max_length=10),
        ),
    ]
