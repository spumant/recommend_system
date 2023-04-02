# Generated by Django 4.1.6 on 2023-03-27 12:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Log",
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
                ("user", models.IntegerField()),
                ("itemid", models.IntegerField()),
                ("tagid", models.IntegerField()),
                ("time", models.IntegerField()),
                ("like", models.IntegerField()),
                ("col", models.IntegerField()),
            ],
            options={
                "db_table": "log",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="Question",
            fields=[
                ("qid", models.IntegerField(primary_key=True, serialize=False)),
                ("title", models.CharField(max_length=255)),
                ("a", models.CharField(max_length=255)),
                ("b", models.CharField(max_length=255)),
                ("c", models.CharField(max_length=255)),
                ("d", models.CharField(max_length=255)),
                ("ans", models.CharField(max_length=255)),
            ],
            options={
                "db_table": "question",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="Special",
            fields=[
                ("id", models.IntegerField(primary_key=True, serialize=False)),
                ("title", models.CharField(max_length=255)),
                ("a", models.CharField(max_length=255)),
                ("b", models.CharField(max_length=255)),
                ("c", models.CharField(max_length=255)),
                ("d", models.CharField(max_length=255)),
                ("ans", models.CharField(max_length=255)),
                ("time", models.CharField(max_length=255)),
                ("name", models.CharField(max_length=255)),
            ],
            options={
                "db_table": "special",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="Users",
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
                ("name", models.CharField(max_length=99)),
                ("password", models.CharField(max_length=99)),
            ],
            options={
                "db_table": "users",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="Week",
            fields=[
                ("id", models.IntegerField(primary_key=True, serialize=False)),
                ("title", models.CharField(max_length=255)),
                ("a", models.CharField(max_length=255)),
                ("b", models.CharField(max_length=255)),
                ("c", models.CharField(max_length=255)),
                ("d", models.CharField(max_length=255)),
                ("ans", models.CharField(max_length=255)),
                ("year", models.IntegerField()),
                ("time", models.IntegerField()),
            ],
            options={
                "db_table": "week",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="Wrong",
            fields=[
                ("userid", models.IntegerField()),
                (
                    "title",
                    models.CharField(db_collation="utf8_general_ci", max_length=255),
                ),
                ("a", models.CharField(db_collation="utf8_general_ci", max_length=255)),
                ("b", models.CharField(db_collation="utf8_general_ci", max_length=255)),
                ("c", models.CharField(db_collation="utf8_general_ci", max_length=255)),
                ("d", models.CharField(db_collation="utf8_general_ci", max_length=255)),
                ("ans", models.CharField(max_length=255)),
                ("id", models.IntegerField(primary_key=True, serialize=False)),
            ],
            options={
                "db_table": "wrong",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="Collection",
            fields=[
                (
                    "id",
                    models.OneToOneField(
                        db_column="id",
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        primary_key=True,
                        serialize=False,
                        to="APP01.users",
                    ),
                ),
                ("collection", models.CharField(max_length=99)),
            ],
            options={
                "db_table": "collection",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="Like",
            fields=[
                (
                    "id",
                    models.OneToOneField(
                        db_column="id",
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        primary_key=True,
                        serialize=False,
                        to="APP01.users",
                    ),
                ),
                ("like", models.CharField(max_length=99)),
            ],
            options={
                "db_table": "like",
                "managed": False,
            },
        ),
    ]