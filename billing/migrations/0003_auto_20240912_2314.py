# Generated by Django 3.0.8 on 2024-09-12 17:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0002_auto_20240912_1122'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_name', models.CharField(max_length=255)),
                ('mobile_number', models.CharField(max_length=50)),
                ('address', models.CharField(blank=True, max_length=250)),
            ],
        ),
        migrations.RemoveField(
            model_name='invoice',
            name='customer_name',
        ),
        migrations.AddField(
            model_name='invoice',
            name='customer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='billing.Customer'),
        ),
    ]
