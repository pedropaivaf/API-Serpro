import sys
import unittest
from fastapi.testclient import TestClient

# Adicionar o diretório atual ao path para importação
sys.path.append('.')

from localhost import app

class TestSerproEndpoints(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_root_endpoint(self):
        print("\n[TEST] GET / (Health Check)")
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        print(f"Status: {data.get('status')}, Versão: {data.get('version')}")
        self.assertEqual(data.get("status"), "online")
        self.assertEqual(data.get("service"), "SERPRO mTLS Proxy")

    def test_autenticar_serpro_trial(self):
        print("\n[TEST] POST /autenticar_serpro (Trial Mode)")
        payload = {
            "consumer_key": "dummy_key",
            "consumer_secret": "dummy_secret",
            "contratante_numero": "00000000000000",
            "autor_pedido_dados_numero": "00000000000",
            "ambiente": "trial"
        }
        response = self.client.post("/autenticar_serpro", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        print(f"Token obtido: {data.get('access_token')[:10]}...")
        self.assertEqual(data.get("access_token"), "06aef429-a981-3ec5-a1f8-71d38d86481e")
        self.assertEqual(data.get("contratante_numero"), "00000000000000")

    def test_autenticar_procurador_trial(self):
        print("\n[TEST] POST /autenticar_procurador (Trial Mode)")
        payload = {
            "consumer_key": "dummy_key",
            "consumer_secret": "dummy_secret",
            "contratante_numero": "00000000000000",
            "contratante_nome": "Empresa Teste",
            "autor_pedido_dados_numero": "00000000000",
            "autor_nome": "Contador Teste",
            "ambiente": "trial"
        }
        response = self.client.post("/autenticar_procurador", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        print(f"Procurador token obtido: {data.get('procurador_token')}")
        self.assertEqual(data.get("procurador_token"), "trial_procurador_token_simulado")
        self.assertEqual(data.get("access_token"), "06aef429-a981-3ec5-a1f8-71d38d86481e")

    def test_proxy_serpro_trial_ccmei(self):
        print("\n[TEST] POST /proxy_serpro (Trial Mode, CCMEI)")
        # O endpoint correto da API do SERPRO é '/Consultar', e o idSistema no body especifica o serviço ('CCMEI')
        payload = {
            "endpoint": "/Consultar",
            "body": {
                "contratante": {
                    "numero": "00000000000000",
                    "tipo": 2
                },
                "autorPedidoDados": {
                    "numero": "00000000000",
                    "tipo": 1
                },
                "contribuinte": {
                    "numero": "00000000000000",
                    "tipo": 2
                },
                "pedidoDados": {
                    "idSistema": "CCMEI",
                    "idServico": "DADOSCCMEI122",
                    "versaoSistema": "1.0",
                    "dados": ""
                }
            },
            "access_token": "06aef429-a981-3ec5-a1f8-71d38d86481e",
            "jwt_token": "06aef429-a981-3ec5-a1f8-71d38d86481e",
            "ambiente": "trial"
        }
        try:
            response = self.client.post("/proxy_serpro", json=payload)
            # Como esse endpoint faz uma requisição HTTP real ao gateway do SERPRO,
            # ele pode retornar 200 se a API do SERPRO trial estiver online e aceitar o token,
            # ou retornar um erro se a rede/API estiver indisponível.
            print(f"Status Code retornado do proxy: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print("Resposta obtida com sucesso do servidor do SERPRO (Trial)!")
                print(f"Chaves na resposta: {list(data.keys())}")
            else:
                print(f"O servidor do SERPRO retornou status {response.status_code}: {response.text}")
        except Exception as e:
            print(f"Erro ao conectar na API externa do SERPRO (Trial): {e}")

if __name__ == "__main__":
    unittest.main()
