# Generated by Django 2.2.2 on 2019-06-16 09:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0002_auto_20190615_2300'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='state',
            field=models.CharField(choices=[('FAILED', 'Upload Failed'), ('FILE_ADDED', 'File Added'), ('IN_PROGRESS', 'Digitization In Progress'), ('DIG_FAILED', 'Digitization Failed'), ('PARTIAL_DIGITIZED', 'Under Review'), ('DIGITIZED', 'Uploaded')], max_length=20),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='state',
            field=models.CharField(choices=[('FILE_ADDED', 'File Added'), ('IN_PROGRESS', 'Digitization In Progress'), ('DIG_FAILED', 'Digitization Failed'), ('PARTIAL_DIGITIZED', 'Under Review'), ('DIGITIZED', 'Uploaded')], max_length=20),
        ),
    ]
