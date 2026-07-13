import sys
import json
from fastapi.testclient import TestClient

# Adicionar o diretório atual ao path para importação
sys.path.append('.')

from localhost import app

def run_tests():
    client = TestClient(app)
    
    print("=" * 70)
    print("    BATERIA COMPLETA DE TESTES DE INTEGRAÇÃO (SERPRO API MOCK)  ")
    print("=" * 70)
    
    # 1. Health check
    print("\n[TEST 1] GET / (Health Check)")
    r = client.get("/")
    assert r.status_code == 200
    print(f"Status: {r.json().get('status')} - OK")

    # 2. Autenticação SERPRO
    print("\n[TEST 2] POST /autenticar_serpro")
    auth_payload = {
        "consumer_key": "dummy_key",
        "consumer_secret": "dummy_secret",
        "contratante_numero": "00000000000000",
        "autor_pedido_dados_numero": "00000000000",
        "ambiente": "trial"
    }
    r = client.post("/autenticar_serpro", json=auth_payload)
    assert r.status_code == 200
    print(f"Status: 200 - Token OAuth2 obtido com sucesso.")

    # 3. Autenticação Procurador
    print("\n[TEST 3] POST /autenticar_procurador")
    proc_payload = {
        "consumer_key": "dummy_key",
        "consumer_secret": "dummy_secret",
        "contratante_numero": "00000000000000",
        "contratante_nome": "Empresa Teste",
        "autor_pedido_dados_numero": "00000000000",
        "autor_nome": "Contador Teste",
        "ambiente": "trial"
    }
    r = client.post("/autenticar_procurador", json=proc_payload)
    assert r.status_code == 200
    print(f"Status: 200 - Token de Procurador obtido com sucesso.")

    # Lista de endpoints/serviços para testar via Proxy
    proxy_tests = [
        {
            "name": "CCMEI - Consultar Dados",
            "endpoint": "/Consultar",
            "idSistema": "CCMEI",
            "idServico": "DADOSCCMEI122",
            "contribuinte": "00000000000000",
            "contribuinte_tipo": 2,
            "dados": ""
        },
        {
            "name": "CCMEI - Emitir Certificado (PDF)",
            "endpoint": "/Emitir",
            "idSistema": "CCMEI",
            "idServico": "EMITIRCCMEI121",
            "contribuinte": "00000000000000",
            "contribuinte_tipo": 2,
            "dados": ""
        },
        {
            "name": "CCMEI - Consultar Situação Cadastral",
            "endpoint": "/Consultar",
            "idSistema": "CCMEI",
            "idServico": "CCMEISITCADASTRAL123",
            "contribuinte": "00000000000",
            "contribuinte_tipo": 1,
            "dados": ""
        },
        {
            "name": "Caixa Postal - Monitorar Novas Mensagens",
            "endpoint": "/Monitorar",
            "idSistema": "CAIXAPOSTAL",
            "idServico": "INNOVAMSG63",
            "contribuinte": "00000000000000",
            "contribuinte_tipo": 2,
            "dados": ""
        },
        {
            "name": "Caixa Postal - Listar Mensagens",
            "endpoint": "/Consultar",
            "idSistema": "CAIXAPOSTAL",
            "idServico": "MSGCONTRIBUINTE61",
            "contribuinte": "00000000000000",
            "contribuinte_tipo": 2,
            "dados": json.dumps({"statusLeitura": 0, "indicadorFavorito": None, "indicadorPagina": 0})
        },
        {
            "name": "Procurações - Obter Procuração Ativa",
            "endpoint": "/Consultar",
            "idSistema": "PROCURACOES",
            "idServico": "OBTERPROCURACAO70",
            "contribuinte": "00000000000000",
            "contribuinte_tipo": 2,
            "dados": ""
        },
        {
            "name": "DTE - Verificar se DTE está Ativo",
            "endpoint": "/Consultar",
            "idSistema": "DTE",
            "idServico": "DTEATIVO60",
            "contribuinte": "00000000000000",
            "contribuinte_tipo": 2,
            "dados": ""
        },
        {
            "name": "PGMEI - Gerar DAS (Mensal)",
            "endpoint": "/Emitir",
            "idSistema": "PGMEI",
            "idServico": "GERARDAS41",
            "contribuinte": "00000000000000",
            "contribuinte_tipo": 2,
            "dados": json.dumps({"periodoApuracao": "202401"})
        },
        {
            "name": "SITFIS - Consultar Situação Fiscal",
            "endpoint": "/Consultar",
            "idSistema": "SITFIS",
            "idServico": "SITFISCOESCRITURAL21",
            "contribuinte": "00000000000000",
            "contribuinte_tipo": 2,
            "dados": ""
        }
    ]

    print("\n" + "=" * 70)
    print("      EXECUTANDO TESTES DOS SERVIÇOS INDIVIDUAIS (VIA PROXY)     ")
    print("=" * 70)

    sucessos = 0
    falhas = 0

    for idx, test in enumerate(proxy_tests, start=4):
        print(f"\n[TEST {idx}] Proxy para: {test['name']}")
        print(f"  - Endpoint: {test['endpoint']}")
        print(f"  - idSistema: {test['idSistema']} | idServico: {test['idServico']}")
        
        payload = {
            "endpoint": test["endpoint"],
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
                    "numero": test["contribuinte"],
                    "tipo": test["contribuinte_tipo"]
                },
                "pedidoDados": {
                    "idSistema": test["idSistema"],
                    "idServico": test["idServico"],
                    "versaoSistema": "1.0",
                    "dados": test["dados"]
                }
            },
            "access_token": "06aef429-a981-3ec5-a1f8-71d38d86481e",
            "jwt_token": "06aef429-a981-3ec5-a1f8-71d38d86481e",
            "ambiente": "trial"
        }
        
        try:
            r = client.post("/proxy_serpro", json=payload)
            if r.status_code == 200:
                print(f"  [SUCCESS] Status: 200 OK")
                resp_json = r.json()
                print(f"  [INFO] Status retornado: {resp_json.get('status')}")
                if resp_json.get("mensagens"):
                    print(f"  [INFO] Mensagem: {resp_json.get('mensagens')}")
                sucessos += 1
            else:
                print(f"  [FAIL] Status: {r.status_code}")
                print(f"  [ERROR] Resposta de Erro: {r.text}")
                falhas += 1
        except Exception as e:
            print(f"  [ERROR] Erro de conexao/execucao: {e}")
            falhas += 1

        # Adiciona delay para evitar 429 (Too Many Requests / Quota Exceeded) do gateway compartilhado
        import time
        time.sleep(2.5)

    print("\n" + "=" * 70)
    print("                       RESUMO DA BATERIA DE TESTES              ")
    print("=" * 70)
    print(f"  Total de testes executados: {3 + len(proxy_tests)}")
    print(f"  [SUCCESS] Sucessos: {3 + sucessos}")
    print(f"  [FAIL] Falhas: {falhas}")
    print("=" * 70)

if __name__ == "__main__":
    run_tests()
