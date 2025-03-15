# Generated by Django 5.1.7 on 2025-03-11 00:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="ConfiguracaoIA",
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
                (
                    "modelo",
                    models.CharField(
                        choices=[
                            ("gpt-3.5-turbo", "GPT-3.5 Turbo"),
                            ("gpt-4", "GPT-4"),
                            ("gpt-4-turbo", "GPT-4 Turbo"),
                            ("claude-3-opus", "Claude 3 Opus"),
                            ("claude-3-sonnet", "Claude 3 Sonnet"),
                            ("claude-3-haiku", "Claude 3 Haiku"),
                        ],
                        default="gpt-3.5-turbo",
                        max_length=50,
                    ),
                ),
                ("temperatura", models.FloatField(default=0.7)),
                ("max_tokens", models.PositiveIntegerField(default=1000)),
                ("chave_api", models.CharField(max_length=255)),
                ("ativo", models.BooleanField(default=True)),
                ("data_criacao", models.DateTimeField(auto_now_add=True)),
                ("data_atualizacao", models.DateTimeField(auto_now=True)),
            ],
            options={
                "verbose_name": "Configuração de IA",
                "verbose_name_plural": "Configurações de IA",
                "ordering": ["nome"],
            },
        ),
        migrations.CreateModel(
            name="Interacao",
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
                ("pergunta", models.TextField()),
                ("resposta", models.TextField()),
                ("tokens_utilizados", models.PositiveIntegerField(default=0)),
                ("data_criacao", models.DateTimeField(auto_now_add=True)),
                (
                    "configuracao_ia",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="interacoes",
                        to="api.configuracaoia",
                    ),
                ),
                (
                    "curso",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="interacoes",
                        to="api.curso",
                    ),
                ),
            ],
            options={
                "verbose_name": "Interação",
                "verbose_name_plural": "Interações",
                "ordering": ["-data_criacao"],
            },
        ),
    ]
