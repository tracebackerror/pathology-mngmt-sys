# Generated by Django 3.0 on 2021-06-19 19:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lab', '0003_test_units'),
    ]

    operations = [
        migrations.AlterField(
            model_name='test',
            name='elabaorated_range',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='test',
            name='notes',
            field=models.TextField(blank=True, null=True),
        ),
    ]
