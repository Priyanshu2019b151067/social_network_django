# Generated by Django 3.2.4 on 2021-06-15 04:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_relationship'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profiles',
            name='avatar',
            field=models.ImageField(default='man.png', upload_to='profiles/'),
        ),
    ]