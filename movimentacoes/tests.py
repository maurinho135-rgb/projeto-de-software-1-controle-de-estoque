from django.test import TestCase

from .models import Movimentacao, Produto
from .services import registrar_movimentacao


class TestIntegracaoEstoque(TestCase):
    def test_saida_grava_movimentacao_e_atualiza_saldo(self):
        produto = Produto.objects.create(nome="Arroz 1 kg", saldo=10)

        registrar_movimentacao(produto.pk, "saida", 3)

        produto.refresh_from_db()
        registro = Movimentacao.objects.get(produto=produto)
        self.assertEqual(produto.saldo, 7)
        self.assertEqual(registro.tipo, "saida")
        self.assertEqual(registro.quantidade, 3)

    def test_saida_acima_do_saldo_nao_altera_o_banco(self):
        produto = Produto.objects.create(nome="Arroz 1 kg", saldo=10)

        with self.assertRaisesRegex(ValueError, "Saldo insuficiente"):
            registrar_movimentacao(produto.pk, "saida", 11)

        produto.refresh_from_db()
        self.assertEqual(produto.saldo, 10)
        self.assertFalse(Movimentacao.objects.filter(produto=produto).exists())