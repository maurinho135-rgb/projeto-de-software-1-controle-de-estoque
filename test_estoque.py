import unittest

from estoque import calcular_novo_saldo


class TestEstoque(unittest.TestCase):
    def test_entrada(self):
        self.assertEqual(calcular_novo_saldo(10, "entrada", 3), 13)

    def test_saida(self):
        self.assertEqual(calcular_novo_saldo(10, "saida", 3), 7)

    def test_saida_de_todo_o_estoque(self):
        self.assertEqual(calcular_novo_saldo(10, "saida", 10), 0)

    def test_saldo_insuficiente(self):
        with self.assertRaisesRegex(ValueError, "Saldo insuficiente"):
            calcular_novo_saldo(10, "saida", 11)

    def test_quantidade_invalida(self):
        for quantidade in (0, -1, 1.5, "3", True):
            with self.subTest(quantidade=quantidade):
                with self.assertRaisesRegex(ValueError, "quantidade inteira"):
                    calcular_novo_saldo(10, "entrada", quantidade)

    def test_tipo_invalido(self):
        with self.assertRaisesRegex(ValueError, "Tipo de movimentação inválido"):
            calcular_novo_saldo(10, "ajuste", 3)