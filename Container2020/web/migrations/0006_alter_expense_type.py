# Generated by Django 3.2.5 on 2021-08-10 21:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0005_feedback'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='type', to='web.type', verbose_name='Choose Type'),
        ),
    ]
