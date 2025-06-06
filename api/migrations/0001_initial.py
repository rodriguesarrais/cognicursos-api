# Generated by Django 5.1.7 on 2025-03-11 00:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Categoria",
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
                ("nome", models.CharField(max_length=100)),
                ("descricao", models.TextField(blank=True, null=True)),
                ("data_criacao", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "verbose_name": "Categoria",
                "verbose_name_plural": "Categorias",
                "ordering": ["nome"],
            },
        ),
        migrations.CreateModel(
            name="Curso",
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
                ("titulo", models.CharField(max_length=200)),
                ("descricao", models.TextField()),
                ("data_publicacao", models.DateTimeField(auto_now_add=True)),
                ("data_atualizacao", models.DateTimeField(auto_now=True)),
                (
                    "nivel",
                    models.CharField(
                        choices=[
                            ("B", "Básico"),
                            ("I", "Intermediário"),
                            ("A", "Avançado"),
                        ],
                        default="B",
                        max_length=1,
                    ),
                ),
                ("carga_horaria", models.PositiveIntegerField()),
                ("ativo", models.BooleanField(default=True)),
                (
                    "categoria",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="cursos",
                        to="api.categoria",
                    ),
                ),
            ],
            options={
                "verbose_name": "Curso",
                "verbose_name_plural": "Cursos",
                "ordering": ["-data_publicacao"],
            },
        ),
    ]
