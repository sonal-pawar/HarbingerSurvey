# Generated by Django 2.1.5 on 2019-02-12 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0003_auto_20190207_1806'),
    ]

    operations = [
        migrations.AddField(
            model_name='surveyfeedback',
            name='flag',
            field=models.BooleanField(default=0),
            preserve_default=False,
        ),
    ]
