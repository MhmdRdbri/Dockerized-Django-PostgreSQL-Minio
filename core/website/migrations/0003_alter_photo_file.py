# Generated by Django 3.2.17 on 2023-02-07 07:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0002_alter_photo_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='file',
            field=models.ImageField(default=None, upload_to='photos/'),
            preserve_default=False,
        ),
    ]
