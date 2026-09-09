import pytest
from unittest.mock import patch, MagicMock
from api import app

@pytest.fixture
def client():
    app.config["TESTING"] == True
    with app.test_client() as client:
        yield client

@patch('api.get_connection')
def test_listar_imoveis_ok(mock_conectar_banco, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [
        (1, 'Nicole Common', 'Travessa', 'Lake Danielle', 'Judymouth', '85184', 'casa em condominio', '488424', '2017-07-29'),
        (2, 'Price Prairie', 'Travessa', 'Colonton', 'North Garyville', '93354', 'casa em condominio', '260070', '2021-11-30'),
    ]

    mock_conectar_banco.return_value = mock_conn

    response = client.get('/imoveis')

    assert response.status_code == 200
    assert response.get_json() == [
        {'id': 1, 'logradouro': 'Nicole Common', 'tipo_logradouro': 'Travessa', 'bairro': 'Lake Danielle', 'cidade': 'Judymouth', 'cep': '85184', 'tipo': 'casa em condominio', 'valor': '488424', 'data_aquisicao': '2017-07-29'},
        {'id': 2, 'logradouro': 'Price Prairie', 'tipo_logradouro': 'Travessa', 'bairro': 'Colonton', 'cidade': 'North Garyville', 'cep': '93354', 'tipo': 'casa em condominio', 'valor': '260070', 'data_aquisicao': '2021-11-30'},
    ]

    mock_cursor.execute.assert_called_once_with(
        "SELECT * FROM imoveis"
    )
    mock_cursor.fetchall.assert_called_once()
    mock_cursor.close.assert_called_once()
    mock_conn.close.assert_called_once()

@patch('api.get_connection')
def test_listar_imoveis_vazio(mock_conectar_banco, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = []

    mock_conectar_banco.return_value = mock_conn

    response = client.get('/imoveis')

    assert response.status_code == 200
    assert response.get_json() == []

    mock_cursor.execute.assert_called_once_with(
        "SELECT * FROM imoveis"
    )
    mock_cursor.fetchall.assert_called_once()
    mock_cursor.close.assert_called_once()
    mock_conn.close.assert_called_once()

@patch('api.get_connection')
def test_listar_imovel_por_id_ok(mock_conectar_banco, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.fetchone.return_value = (1, 'Nicole Common', 'Travessa', 'Lake Danielle', 'Judymouth', '85184', 'casa em condominio', '488424', '2017-07-29')
    mock_conectar_banco.return_value = mock_conn

    response = client.get('/imoveis/1')

    assert response.status_code == 200
    assert response.get_json() == {'id': 1, 'logradouro': 'Nicole Common', 'tipo_logradouro': 'Travessa', 'bairro': 'Lake Danielle', 'cidade': 'Judymouth', 'cep': '85184', 'tipo': 'casa em condominio', 'valor': '488424', 'data_aquisicao': '2017-07-29'}

    mock_cursor.execute.assert_called_once_with(
        "SELECT * FROM imoveis WHERE id = %s",
        (1,)
    )

    mock_cursor.fetchone.assert_called_once()
    mock_cursor.close.assert_called_once()
    mock_conn.close.assert_called_once()

@patch('api.get_connection')
def test_listar_imovel_por_id_erro(mock_conectar_banco, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.fetchone.return_value = None
    mock_conectar_banco.return_value = mock_conn

    response = client.get('/imoveis/999')

    assert response.status_code == 404
    assert response.get_json() == {'erro': 'Imóvel não encontrado'}

    mock_cursor.execute.assert_called_once_with(
        "SELECT * FROM imoveis WHERE id = %s",
        (999,)
    )

    mock_cursor.fetchone.assert_called_once()
    mock_cursor.close.assert_called_once()
    mock_conn.close.assert_called_once()

@patch('api.get_connection')
def test_adicionar_imovel_ok(mock_conectar_banco, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.lastrowid = 10

    mock_conectar_banco.return_value = mock_conn

    payload = {'logradouro': 'Nicole Common', 'tipo_logradouro': 'Travessa', 'bairro': 'Lake Danielle', 'cidade': 'Judymouth', 'cep': '85184', 'tipo': 'casa em condominio', 'valor': '488424', 'data_aquisicao': '2017-07-29'}
    response = client.post('/imoveis', json=payload)

    assert response.status_code == 201
    assert response.get_json() == {'id': 10}

    mock_cursor.execute.assert_called_once_with(
        "INSERT INTO imoveis (logradouro, tipo_logradouro, bairro, cidade, cep, tipo, valor, data_aquisicao) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
        ('Nicole Common', 'Travessa', 'Lake Danielle', 'Judymouth', '85184', 'casa em condominio', '488424', '2017-07-29')
    )
    mock_conn.commit.assert_called_once()
    mock_cursor.close.assert_called_once()
    mock_conn.close.assert_called_once()

@patch('api.get_connection')
def test_adicionar_imovel_erro(mock_conectar_banco, client):
    response = client.post('/imoveis', json={'logradouro': 'blablabla'})

    assert response.status_code == 400
    assert response.get_json() == {'erro': 'Campos obrigatórios: logradouro, tipo_logradouro, bairro, cidade, cep, tipo, valor, data_aquisicao'}

    mock_conectar_banco.assert_not_called()

@patch('api.get_connection')
def test_atualizar_imovel_ok(mock_conectar_banco, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.rowcount = 1
    mock_conectar_banco.return_value = mock_conn

    payload = {'logradouro': 'Rafael Duarte', 'tipo_logradouro': 'sei la', 'bairro': 'ulala', 'cidade': 'sp né', 'cep': '01201', 'tipo': 'mansao', 'valor': '000999', 'data_aquisicao': '2026-05-09'}
    response = client.put('/imoveis/1', json=payload)

    assert response.status_code == 200
    assert response.get_json() == {'mensagem': 'Imóvel atualizado com sucesso'}

    mock_cursor.execute.assert_called_once_with(
        "UPDATE imoveis SET logradouro = %s, tipo_logradouro = %s, bairro = %s, cidade = %s, cep = %s, tipo = %s, valor = %s, data_aquisicao = %s WHERE id = %s",
        ('Rafael Duarte', 'sei la', 'ulala', 'sp né', '01201', 'mansao', '000999', '2026-05-09', 1)
    )
    mock_conn.commit.assert_called_once()
    mock_cursor.close.assert_called_once()
    mock_conn.close.assert_called_once()

@patch('api.get_connection')
def test_atualizar_imovel_not_found(mock_conectar_banco, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.rowcount = 0
    mock_conectar_banco.return_value = mock_conn

    payload = {'logradouro': 'Rafael Duarte', 'tipo_logradouro': 'sei la', 'bairro': 'ulala', 'cidade': 'sp né', 'cep': '01201', 'tipo': 'mansao', 'valor': '000999', 'data_aquisicao': '2026-05-09'}
    response = client.put('/imoveis/999', json=payload)

    assert response.status_code == 404
    assert response.get_json() == {'erro': 'Imóvel não encontrado'}

    mock_cursor.execute.assert_called_once_with(
        "UPDATE imoveis SET logradouro = %s, tipo_logradouro = %s, bairro = %s, cidade = %s, cep = %s, tipo = %s, valor = %s, data_aquisicao = %s WHERE id = %s",
        ('Rafael Duarte', 'sei la', 'ulala', 'sp né', '01201', 'mansao', '000999', '2026-05-09', 999)
    )

    mock_conn.commit.assert_called_once()
    mock_cursor.close.assert_called_once()
    mock_conn.close.assert_called_once()

@patch('api.get_connection')
def test_atualizar_imovel_erro(mock_conectar_banco, client):
    response = client.put('/imoveis/1', json={'logradouro': 'só isso tb nao da né'})

    assert response.status_code == 400
    assert response.get_json() == {'erro': 'Campos obrigatórios: logradouro, tipo_logradouro, bairro, cidade, cep, tipo, valor, data_aquisicao'}

    mock_conectar_banco.assert_not_called()

@patch('api.get_connection')
def test_remover_imovel_ok(mock_conectar_banco, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.rowcount = 1
    mock_conectar_banco.return_value = mock_conn

    response = client.delete('/imoveis/1')

    assert response.status_code == 200
    assert response.get_json() == {'mensagem': 'Imóvel removido com sucesso'}

    mock_cursor.execute.assert_called_once_with(
        "DELETE FROM imoveis WHERE id = %s",
        (1,)
    )
    mock_conn.commit.assert_called_once()
    mock_cursor.close.assert_called_once()
    mock_conn.close.assert_called_once()

@patch('api.get_connection')
def test_remover_imovel_not_found(mock_conectar_banco, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.rowcount = 0
    mock_conectar_banco.return_value = mock_conn

    response = client.delete('/imoveis/999')

    assert response.status_code == 404
    assert response.get_json() == {'erro': 'Imóvel não encontrado'}

    mock_cursor.execute_assert_called_once_with(
        "DELETE FROM imoveis WHERE id = %s",
        (999,)
    )

    mock_conn.commit.assert_called_once()
    mock_cursor.close.assert_called_once()
    mock_conn.close.assert_called_once()

@patch('api.get_connection')
def test_listar_imoveis_por_tipo_ok(mock_conectar_banco, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.fetchall.return_value = [(1, 'Nicole Common', 'Travessa', 'Lake Danielle', 'Judymouth', '85184', 'casa em condominio', '488424', '2017-07-29')]
    mock_conectar_banco.return_value = mock_conn

    response = client.get('/imoveis/tipo/casa em condominio')

    assert response.status_code == 200
    assert response.get_json() == [{'id': 1, 'logradouro': 'Nicole Common', 'tipo_logradouro': 'Travessa', 'bairro': 'Lake Danielle', 'cidade': 'Judymouth', 'cep': '85184', 'tipo': 'casa em condominio', 'valor': '488424', 'data_aquisicao': '2017-07-29'}]

    mock_cursor.execute.assert_called_once_with(
        "SELECT * FROM imoveis WHERE tipo = %s",
        ('casa em condominio',)
    )
    mock_cursor.fetchall.assert_called_once()
    mock_cursor.close.assert_called_once()
    mock_conn.close.assert_called_once()

@patch('api.get_connection')
def test_listar_imoveis_por_tipo_not_found(mock_conectar_banco, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.fetchall.return_value = None
    mock_conectar_banco.return_value = mock_conn

    response = client.get('/imoveis/tipo/lalala')

    assert response.status_code == 404
    assert response.get_json() == {'erro': 'Nenhum imóvel encontrado'}

    mock_cursor.execute.assert_called_once_with(
        "SELECT * FROM imoveis WHERE tipo = %s",
        ('lalala',)
    )
    mock_cursor.fetchall.assert_called_once()
    mock_cursor.close.assert_called_once()
    mock_conn.close.assert_called_once()

@patch('api.get_connection')
def test_listar_imoveis_por_cidade_ok(mock_conectar_banco, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.fetchall.return_value = [(1, 'Nicole Common', 'Travessa', 'Lake Danielle', 'Judymouth', '85184', 'casa em condominio', '488424', '2017-07-29')]
    mock_conectar_banco.return_value = mock_conn

    response = client.get('/imoveis/cidade/Judymouth')

    assert response.status_code == 200
    assert response.get_json() == [{'id': 1, 'logradouro': 'Nicole Common', 'tipo_logradouro': 'Travessa', 'bairro': 'Lake Danielle', 'cidade': 'Judymouth', 'cep': '85184', 'tipo': 'casa em condominio', 'valor': '488424', 'data_aquisicao': '2017-07-29'}]

    mock_cursor.execute.assert_called_once_with(
        "SELECT * FROM imoveis WHERE cidade = %s",
        ('Judymouth',)
    )
    mock_cursor.fetchall.assert_called_once()
    mock_cursor.close.assert_called_once()
    mock_conn.close.assert_called_once()

@patch('api.get_connection')
def test_listar_imoveis_por_cidade_not_found(mock_conectar_banco, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.fetchall.return_value = None
    mock_conectar_banco.return_value = mock_conn

    response = client.get('/imoveis/cidade/uiuiui')

    assert response.status_code == 404
    assert response.get_json() == {'erro': 'Nenhum imóvel encontrado'}

    mock_cursor.execute.assert_called_once_with(
        "SELECT * FROM imoveis WHERE cidade = %s",
        ('uiuiui',)
    )
    mock_cursor.fetchall.assert_called_once()
    mock_cursor.close.assert_called_once()
    mock_conn.close.assert_called_once()