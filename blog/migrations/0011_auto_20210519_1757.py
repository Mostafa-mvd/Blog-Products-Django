# Generated by Django 3.2 on 2021-05-19 17:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0010_auto_20210519_1041'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='dislike_btn_clicked',
            field=models.BooleanField(auto_created=True, default=False),
        ),
        migrations.AlterField(
            model_name='post',
            name='like_btn_clicked',
            field=models.BooleanField(auto_created=True, default=False),
        ),
    ]
