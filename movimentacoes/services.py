from django.db import transaction

from estoque import calcular_novo_saldo
from .models import Movimentacao, Produto


@transaction.atomic
def registrar_movimentacao(produto_id, tipo, quantidade):
    produto = Produto.objects.select_for_update().get(pk=produto_id)
    produto.saldo = calcular_novo_saldo(produto.saldo, tipo, quantidade)
    produto.save(update_fields=["saldo"])
    return Movimentacao.objects.create(
        produto=produto, tipo=tipo, quantidade=quantidade
    )