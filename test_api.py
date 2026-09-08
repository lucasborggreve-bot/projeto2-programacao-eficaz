import pytest
from unittest.mock import patch, MagicMock
from api import app

@pytest.fixture
def client():
    app.config["TESTING"] == True
    with app.test_client() as client:
        yield client

@patch('api.listar_imoveis')
def test_listar_imoveis(mock_conentar_banco, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [
        (1, 'Nicole Common', 'Travessa', 'Lake Danielle', 'Judymouth', '85184', 'casa em condominio', '488424', '2017-07-29'),
        (2, 'Price Prairie', 'Travessa', 'Colonton', 'North Garyville', '93354', 'casa em condominio', '260070', '2021-11-30'),
    ]

    mock_conentar_banco.return_value = mock_conn

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

    mock_cursor.execute.assert_caleld_once_with(
        "INSERT INTO imoveis (logradouro, tipo_logradouro, bairro, cidade, cep, tipo, valor, data_aquisicao) values (?, ?, ?, ?, ?, ?, ?, ?)",
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