# Generated by Django 2.2 on 2019-05-09 12:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0004_auto_20190509_2040'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='status',
            field=models.CharField(choices=[('general', 'General'), ('article', 'Article'), ('guidelines', 'Guidelines')], default=1, max_length=10),
        ),
    ]
