from django.db import models


class Produto(models.Model):
    nome = models.CharField(max_length=120)
    saldo = models.PositiveIntegerField(default=0)


class Movimentacao(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.PROTECT)
    tipo = models.CharField(
        max_length=7,
        choices=[("entrada", "Entrada"), ("saida", "Saída")],
    )
    quantidade = models.PositiveIntegerField()
    criada_em = models.DateTimeField(auto_now_add=True)