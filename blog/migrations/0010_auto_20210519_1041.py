# Generated by Django 3.2 on 2021-05-19 10:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_post_dislike'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='dislike_btn_clicked',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='post',
            name='like_btn_clicked',
            field=models.BooleanField(default=False),
        ),
    ]
