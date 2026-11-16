def validar_quantidade(quantidade):
    if type(quantidade) is not int or quantidade <= 0:
        raise ValueError("Informe uma quantidade inteira maior que zero.")


def calcular_novo_saldo(saldo_atual, tipo, quantidade):
    validar_quantidade(quantidade)

    if tipo == "entrada":
        return saldo_atual + quantidade

    if tipo == "saida":
        if quantidade > saldo_atual:
            raise ValueError("Saldo insuficiente para a saída.")
        return saldo_atual - quantidade

    raise ValueError("Tipo de movimentação inválido. Use entrada ou saida.")
