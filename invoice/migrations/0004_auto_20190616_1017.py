# Generated by Django 2.2.2 on 2019-06-16 10:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0003_auto_20190616_0901'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='due',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='paid',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='refund',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='sub_total',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='tax',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='total',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True),
        ),
    ]