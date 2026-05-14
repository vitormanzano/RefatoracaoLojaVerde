import pytest
from pathlib import Path


from legacy import Sis
from legacy import PedEspecial

# Comandos
# python -m pytest -v
# coverage: 
# python -m pytest --cov=. --cov-report=term-missing --cov-report=html


@pytest.fixture
def sis(tmp_path, monkeypatch):
    """Isola o banco em diretorio temporario por teste."""
    monkeypatch.chdir(tmp_path)
    s = Sis()
    yield s
    s.close()
    

@pytest.fixture
def pedEspecial(tmp_path, monkeypatch):
    """Isola o banco em diretorio temporario por teste."""
    monkeypatch.chdir(tmp_path)
    pe = PedEspecial()
    yield pe
    pe.close()



def test_pedido_normal_calcula_total_corretamente(sis):
    itens = [
        {"nome": "p1", "p": 100, "q": 2, "tipo": "normal"},
        {"nome": "p2", "p": 50, "q": 1, "tipo": "desc10"},
        {"nome": "p3", "p": 50, "q": 1, "tipo": "desc20"},
        {"nome": "p4", "p": 50, "q": 1, "tipo": "frete_gratis"},
    ]

    id_ped = sis.add_ped("Joao Silva", itens, "normal")
    pedido = sis.get_ped(id_ped)

    assert pedido["tot"] == pytest.approx(335.0)
    assert pedido["st"] == "pendente"


def test_pedido_vip_aplica_desconto_de_5_por_cento(sis):
    itens = [{"nome": "p1", "p": 100, "q": 1, "tipo": "normal"}]

    id_ped = sis.add_ped("Maria", itens, "vip")
    pedido = sis.get_ped(id_ped)

    assert pedido["tot"] == pytest.approx(95.0)

def test_pedido_corporativo_aplica_desconto_de_10_por_cento(sis):
    itens = [{ "nome": "p1", "p": 100, "q": 1, "tipo": "normal"}]

    id_ped = sis.add_ped("Maria", itens, "corporativo")
    pedido = sis.get_ped(id_ped)

    assert pedido["tot"] == pytest.approx(90.0)


def test_processamento_pagamento_cartao_pedido_inexistente(sis):
    assert sis.proc_pag("Id inexistente", "cartao", 100) is False


def test_processamento_pagamento_cartao(sis):
    itens = [{"nome": "p1", "p": 100, "q": 1, "tipo": "normal"}]

    id_ped = sis.add_ped("Maria", itens, "normal")

    assert sis.proc_pag(id_ped, "cartao", 100) is True


def test_processamento_pagamento_pix(sis):
    itens = [{"nome": "p1", "p": 100, "q": 1, "tipo": "normal"}]

    id_ped = sis.add_ped("Maria", itens, "normal")

    assert sis.proc_pag(id_ped, "pix", 100) is True


def test_processamento_pagamento_boleto(sis):
    itens = [{"nome": "p1", "p": 100, "q": 1, "tipo": "normal"}]

    id_ped = sis.add_ped("Maria", itens, "normal")

    assert sis.proc_pag(id_ped, "boleto", 100) is True


def test_processamento_pagamento_metodo_invalido(sis):
    itens = [{"nome": "p1", "p": 100, "q": 1, "tipo": "normal"}]

    id_ped = sis.add_ped("Maria", itens, "normal")

    assert sis.proc_pag(id_ped, "credito", 100) is False


def test_pagamento_insuficiente_falha(sis):
    itens = [{"nome": "p1", "p": 100, "q": 1, "tipo": "normal"}]

    id_ped = sis.add_ped("Joao", itens, "normal")

    assert sis.proc_pag(id_ped, "cartao", 50) is False

def test_atualizar_status_pedido_existente_para_aprovado(sis):
    itens = [{"nome": "p1", "p": 100, "q": 1, "tipo": "normal"}]

    id_ped = sis.add_ped("Joao", itens, "normal")

    sis.upd_st(id_ped, "aprovado") 

    ped = sis.get_ped(id_ped)

    assert ped['st'] == "aprovado"


def test_atualizar_status_pedido_existente_para_aprovado_cliente_vip(sis):
    itens = [{"nome": "p1", "p": 100, "q": 1, "tipo": "normal"}]

    id_ped = sis.add_ped("Joao", itens, "vip")

    sis.upd_st(id_ped, "aprovado") 

    ped = sis.get_ped(id_ped)

    assert ped['st'] == "aprovado"


def test_atualizar_status_pedido_existente_para_enviado(sis):
    itens = [{"nome": "p1", "p": 100, "q": 1, "tipo": "normal"}]

    id_ped = sis.add_ped("Joao", itens, "normal")

    sis.upd_st(id_ped, "enviado") 

    ped = sis.get_ped(id_ped)

    assert ped['st'] == "enviado"


def test_atualizar_status_pedido_existente_para_entregue_cliente_normal(sis):
    itens = [{"nome": "p1", "p": 100, "q": 1, "tipo": "normal"}]

    id_ped = sis.add_ped("Joao", itens, "normal")

    sis.upd_st(id_ped, "entregue") 

    ped = sis.get_ped(id_ped)

    assert ped['st'] == "entregue"


def test_atualizar_status_pedido_existente_para_entregue_cliente_vip(sis):
    itens = [{"nome": "p1", "p": 100, "q": 1, "tipo": "normal"}]

    id_ped = sis.add_ped("Joao", itens, "vip")

    sis.upd_st(id_ped, "entregue") 

    ped = sis.get_ped(id_ped)

    assert ped['st'] == "entregue"


def test_atualizar_status_pedido_existente_para_entregue_cliente_corporativo(sis):
    itens = [{"nome": "p1", "p": 100, "q": 1, "tipo": "normal"}]

    id_ped = sis.add_ped("Joao", itens, "corporativo")

    sis.upd_st(id_ped, "entregue") 

    ped = sis.get_ped(id_ped)

    assert ped['st'] == "entregue"


# Código simplesmente não diz nada sobre o que aconteceu, se falhou ou se teve sucesso
def test_atualizar_status_pedido_inexistente_para_enviado(sis):
    itens = [{"nome": "p1", "p": 100, "q": 1, "tipo": "normal"}]

    assert sis.upd_st("id_nao_existe", "enviado") == None
    

def test_calcula_valor_total_dos_pedidos_de_um_cliente(sis):
    itens = [{"nome": "p1", "p": 100, "q": 1, "tipo": "normal"}]

    id_ped = sis.add_ped("Joao", itens, "normal")

    valor_total = sis.calc_tot_cli("Joao")

    assert valor_total == pytest.approx(100.0)



def test_cancelar_pedido_existente(sis):
    itens = [{"nome": "p1", "p": 100, "q": 1, "tipo": "normal"}]

    id_ped = sis.add_ped("Joao", itens, "normal")

    sis.cancelar_pedido(id_ped) 

    ped = sis.get_ped(id_ped)

    assert ped['st'] == "cancelado"


def test_cancelar_pedido_inexistente(sis):
    itens = [{"nome": "p1", "p": 100, "q": 1, "tipo": "normal"}]

    assert sis.cancelar_pedido("id_ped") == None

def test_gerar_relatorio_tipo_vendas(sis, tmp_path):
      sis.gerar_rel("vendas")

      arquivo = tmp_path / "rel_vendas.txt"
      assert arquivo.exists()


def test_validar_estoque_com_itens_existentes(sis):
    itens = [{"nome": "produto1", "p": 100, "q": 1, "tipo": "normal"}]

    assert sis.validar_estoque(itens) == True


def test_validar_estoque_com_itens_ineexistentes(sis):
    itens = [{"nome": "produtoinexistente", "p": 100, "q": 1, "tipo": "normal"}]

    assert sis.validar_estoque(itens) == False


def test_validar_estoque_com_itens_existentes_sem_estoque(sis):
    itens = [{"nome": "produto1", "p": 100, "q": 200, "tipo": "normal"}]

    assert sis.validar_estoque(itens) == False



def test_gerar_relatorio_tipo_vendas_com_2_produtos(sis, tmp_path):
    itens = [
            {"nome": "p1", "p": 100, "q": 1, "tipo": "normal"},
            {"nome": "p2", "p": 50, "q": 1, "tipo": "normal"}
    ]

    sis.add_ped("joao", itens, "normal")

    sis.gerar_rel("vendas")

    arquivo = tmp_path / "rel_vendas.txt"
    assert arquivo.exists()
    

def test_gerar_relatorio_tipo_clientes(sis, tmp_path):
      sis.gerar_rel("clientes")

      arquivo = tmp_path / "rel_clientes.txt"
      assert arquivo.exists()


def test_gerar_relatorio_tipo_clientes_com_2_produtos(sis, tmp_path):
    itens = [
            {"nome": "p1", "p": 100, "q": 1, "tipo": "normal"},
            {"nome": "p2", "p": 50, "q": 1, "tipo": "normal"}
    ]

    sis.add_ped("joao", itens, "normal")

    sis.gerar_rel("clientes")

    arquivo = tmp_path / "rel_clientes.txt"
    assert arquivo.exists()
    

def test_pix_aprova_pedido_automaticamente(sis):
    itens = [{"nome": "p1", "p": 100, "q": 1, "tipo": "normal"}]

    id_ped = sis.add_ped("Joao", itens, "normal")
    sis.proc_pag(id_ped, "pix", 100)

    assert sis.get_ped(id_ped)["st"] == "aprovado"


def test_boleto_nao_aprova_automaticamente(sis):
    itens = [{"nome": "p1", "p": 100, "q": 1, "tipo": "normal"}]

    id_ped = sis.add_ped("Joao", itens, "normal")
    sis.proc_pag(id_ped, "boleto", 100)

    assert sis.get_ped(id_ped)["st"] == "pendente"


def test_pedido_especial_calcula_total_corretamente(pedEspecial):
    itens = [
        {"nome": "p1", "p": 100, "q": 2, "tipo": "normal"},
        {"nome": "p2", "p": 50, "q": 1, "tipo": "desc10"},
        {"nome": "p3", "p": 50, "q": 1, "tipo": "desc20"},
    ]

    id_ped = pedEspecial.add_ped("Joao Silva", itens, "normal")
    pedido = pedEspecial.get_ped(id_ped)

    assert pedido["tot"] == pytest.approx(327.75)
    assert pedido["st"] == "pendente"


def test_atualizar_pedido_especial_existente(pedEspecial):

    itens = [
        {"nome": "p1", "p": 100, "q": 2, "tipo": "normal"},
        {"nome": "p2", "p": 50, "q": 1, "tipo": "desc10"},
        {"nome": "p3", "p": 50, "q": 1, "tipo": "desc20"},
    ]

    id_ped = pedEspecial.add_ped("Joao Silva", itens, "normal")
    pedEspecial.upd_st(id_ped, "atualizado")
    pedido = pedEspecial.get_ped(id_ped)

    assert pedido["st"] == "atualizado"


def test_atualizar_pedido_especial_inexistente(pedEspecial):
    assert pedEspecial.upd_st("id_ped", "atualizado") == None


