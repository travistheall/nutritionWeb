# Generated by Django 3.0.6 on 2020-05-25 17:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recurapp', '0004_auto_20200525_1210'),
    ]

    operations = [
        migrations.AlterField(
            model_name='foodweights',
            name='subcode',
            field=models.ForeignKey(blank=True, db_column='Subcode', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subcodedescs', to='recurapp.Subcodedesc'),
        ),
    ]