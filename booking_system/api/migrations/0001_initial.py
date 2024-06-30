# Generated by Django 5.0.6 on 2024-06-29 16:53

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="ZoomMeeting",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("meeting_id", models.CharField(max_length=255, unique=True)),
                ("topic", models.CharField(max_length=255)),
                ("start_time", models.DateTimeField(db_index=True)),
                ("end_time", models.DateTimeField(db_index=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="zoom_meetings",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Booking",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="bookings",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "zoom_meeting",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="bookings",
                        to="api.zoommeeting",
                    ),
                ),
            ],
        ),
        migrations.AddIndex(
            model_name="zoommeeting",
            index=models.Index(
                fields=["user", "start_time"], name="api_zoommee_user_id_4d9444_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="zoommeeting",
            index=models.Index(
                fields=["user", "end_time"], name="api_zoommee_user_id_b2917c_idx"
            ),
        ),
        migrations.AlterUniqueTogether(
            name="booking",
            unique_together={("user", "zoom_meeting")},
        ),
    ]
