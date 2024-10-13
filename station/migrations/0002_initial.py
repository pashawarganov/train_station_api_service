# Generated by Django 4.0.4 on 2024-10-13 13:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('station', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='journey',
            name='crew',
            field=models.ManyToManyField(blank=True, related_name='journeys', to='station.crew'),
        ),
        migrations.AddField(
            model_name='journey',
            name='route',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='journeys', to='station.route'),
        ),
        migrations.AddField(
            model_name='journey',
            name='train',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='journeys', to='station.train'),
        ),
        migrations.AlterUniqueTogether(
            name='ticket',
            unique_together={('journey', 'cargo', 'seat')},
        ),
    ]