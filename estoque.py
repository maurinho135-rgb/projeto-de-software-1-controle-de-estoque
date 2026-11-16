def calcular_novo_saldo(saldo_atual, tipo, quantidade):
    if quantidade <= 0:
        raise ValueError("A quantidade deve ser maior que zero.")

    if tipo == "entrada":
        return saldo_atual + quantidade

    if tipo == "saida":
        if quantidade > saldo_atual:
            raise ValueError("Saldo insuficiente para a saída.")
        return saldo_atual - quantidade

    raise ValueError("Informe entrada ou saida.")
