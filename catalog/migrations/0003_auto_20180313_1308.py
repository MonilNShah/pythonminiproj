# Generated by Django 2.0.2 on 2018-03-13 07:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_auto_20180310_2010'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='book_pic',
            field=models.FileField(upload_to='profilepics/'),
        ),
    ]
