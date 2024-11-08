# Generated by Django 5.1.3 on 2024-11-08 04:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('designapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('category', models.CharField(max_length=255)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(max_length=50)),
            ],
        ),
    ]
