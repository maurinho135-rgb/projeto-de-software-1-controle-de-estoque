
from django import forms
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import redirect, render

from .models import Movimentacao, Produto
from .services import registrar_movimentacao


class CadastroProduto(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ["nome", "saldo"]
        labels = {"saldo": "Saldo inicial"}


class RegistroMovimentacao(forms.Form):
    produto = forms.ModelChoiceField(
        queryset=Produto.objects.order_by("nome"),
        label="Produto",
    )
    tipo = forms.ChoiceField(
        choices=[("entrada", "Entrada"), ("saida", "Saída")]
    )
    quantidade = forms.IntegerField(min_value=1)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["produto"].label_from_instance = lambda produto: (
            f"{produto.nome} — {produto.saldo} unidades"
        )


@staff_member_required
def estoque(request):
    acao = request.POST.get("acao")
    cadastro = CadastroProduto(request.POST if acao == "cadastro" else None)
    registro = RegistroMovimentacao(request.POST if acao == "registro" else None)

    if acao == "cadastro" and cadastro.is_valid():
        cadastro.save()
        return redirect("/?resultado=produto")

    if acao == "registro" and registro.is_valid():
        dados = registro.cleaned_data
        try:
            registrar_movimentacao(
                dados["produto"].pk, dados["tipo"], dados["quantidade"]
            )
        except ValueError as erro:
            registro.add_error("quantidade", str(erro))
        except Produto.DoesNotExist:
            registro.add_error("produto", "Produto não encontrado.")
        else:
            return redirect("/?resultado=movimentacao")

    return render(request, "estoque.html", {
        "cadastro": cadastro,
        "registro": registro,
        "produtos": Produto.objects.order_by("nome"),
        "historico": Movimentacao.objects.select_related("produto").order_by("-pk")[:20],
        "resultado": request.GET.get("resultado"),
    })
