# Generated by Django 3.2 on 2021-05-07 11:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_alter_post_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='', verbose_name='my_post_image'),
        ),
    ]
