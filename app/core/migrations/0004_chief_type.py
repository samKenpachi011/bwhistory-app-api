# Generated by Django 4.0.10 on 2023-06-05 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_chief'),
    ]

    operations = [
        migrations.AddField(
            model_name='chief',
            name='type',
            field=models.CharField(blank=True, choices=[('paramount', 'Paramount'), ('subchief', 'Sub Chief'), ('divisional', 'Divisional')], max_length=100),
        ),
    ]
