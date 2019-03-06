# Generated by Django 2.1.7 on 2019-02-28 12:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='surveyquestion',
            name='question',
        ),
        migrations.AddField(
            model_name='surveyquestion',
            name='question',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='survey.Question'),
            preserve_default=False,
        ),
    ]