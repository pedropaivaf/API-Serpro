# Guia de Integração: ERP + SERPRO + Questor + Acessórias

Este guia orienta o desenvolvedor sobre como acoplar o pacote `serpro_integra_contador_api` no ERP principal e coordenar fluxos integrados com as APIs da **Questor** e da **Acessórias** dentro do mesmo ecossistema.

---

## 1. Importando o Pacote no seu ERP (Dart/Flutter)

Como este projeto é um pacote Dart isolado, você pode acoplá-lo no `pubspec.yaml` do seu projeto principal (ERP) referenciando-o localmente (se estiverem na mesma máquina/repositório monorepo) ou via Git.

### Opção A: Referência por Caminho Local (Monorepo)
Se você clonar ou mover a pasta `API-Serpro` para dentro do diretório do seu ERP, declare assim no `pubspec.yaml` do ERP:

```yaml
dependencies:
  flutter:
    sdk: flutter
  
  # Importando o pacote da API Serpro por caminho relativo
  serpro_integra_contador_api:
    path: ./caminho/para/API-Serpro
```

### Opção B: Referência via Git (Repositórios Separados)
Você pode referenciar diretamente o seu fork do GitHub:

```yaml
dependencies:
  serpro_integra_contador_api:
    git:
      url: https://github.com/pedropaivaf/API-Serpro.git
      ref: main # ou o commit/tag específico
```

---

## 2. Configurando o Ambiente de Desenvolvimento (Com ou Sem Certificado)

Para desenvolver sem travar a máquina com certificados reais e evitar custos em produção, configure o `ApiClient` para utilizar o servidor mock local FastAPI que testamos.

### Configuração em Desenvolvimento (Mock/FastAPI)
Durante o desenvolvimento, aponte a biblioteca para o seu servidor Python local (que roda na porta `8000`):

```dart
import 'package:serpro_integra_contador_api/serpro_integra_contador_api.dart';

void main() async {
  final apiClient = ApiClient();

  // Redireciona todas as requisições para o seu servidor local FastAPI
  apiClient.setServidores(
    urlProxy: 'http://localhost:8000',
    urlAutenticacao: 'http://localhost:8000',
    urlAutenticacaoProcurado: 'http://localhost:8000',
  );

  // Autenticação fictícia (Trial) - NÃO precisa de certificado real
  await apiClient.authenticate(
    consumerKey: '06aef429-a981-3ec5-a1f8-71d38d86481e',
    consumerSecret: '06aef429-a981-3ec5-a1f8-71d38d86481e',
    contratanteNumero: '00000000000000',
    autorPedidoDadosNumero: '00000000000000',
    ambiente: 'trial', // Garante uso da sandbox
  );
}
```

### Configuração em Produção (Direto com Certificado)
Em produção, remova as URLs do proxy para que a biblioteca se conecte diretamente e de forma segura ao gateway real do SERPRO usando o certificado digital do cliente:

```dart
// Em produção, remova o setServidores() para usar a conexão direta do SDK
await apiClient.authenticate(
  consumerKey: 'SUA_KEY_REAL',
  consumerSecret: 'SEU_SECRET_REAL',
  contratanteNumero: 'CNPJ_CLIENTE',
  autorPedidoDadosNumero: 'CPF_OU_CNPJ_CONTADOR',
  certificadoDigitalPath: '/caminho/certificado.p12',
  senhaCertificado: 'senha123',
  ambiente: 'producao',
);
```

---

## 3. Padrão de Projeto: Orquestrador Fiscal (Exemplo Prático)

Para integrar as três APIs (**SERPRO**, **Questor**, e **Acessórias**), o padrão de projeto recomendado é o **Orquestrador (Facade/Orchestrator)**. Ele encapsula as chamadas de cada API e lida com o fluxo de dados unificado.

Aqui está um exemplo conceitual de como estruturar essa classe no seu ERP em Dart:

```dart
import 'package:serpro_integra_contador_api/serpro_integra_contador_api.dart';

// Mocks representativos das suas APIs existentes
class QuestorApi {
  Future<void> registrarLancamentoTributario({required String cnpj, required String periodo, required double valor, required String linhaDigitavel}) async {
    // Sua lógica de integração com a API Questor
    print('Questor: Lançamento tributário registrado para $cnpj ($periodo) - R\$ $valor');
  }
}

class AcessoriasApi {
  Future<void> enviarGuiaAoCliente({required String cnpj, required String nomeArquivo, required String pdfBase64}) async {
    // Sua lógica de integração com a API Acessórias
    print('Acessórias: Guia $nomeArquivo enviada com sucesso para o cliente $cnpj.');
  }
}

/// Orquestrador responsável por coordenar a captura, registro e entrega fiscal
class OrquestradorFiscal {
  final ApiClient _apiClient;
  final QuestorApi _questorApi;
  final AcessoriasApi _acessoriasApi;

  OrquestradorFiscal({
    required ApiClient apiClient,
    required QuestorApi questorApi,
    required AcessoriasApi acessoriasApi,
  })  : _apiClient = apiClient,
        _questorApi = questorApi,
        _acessoriasApi = acessoriasApi;

  /// Fluxo Completo: Emite o DAS (SERPRO), lança no financeiro (Questor) e envia ao cliente (Acessórias)
  Future<bool> processarFechamentoMensalMEI(String cnpjMei, String periodoApuracao) async {
    print('--- Iniciando processamento fiscal para CNPJ: $cnpjMei | Período: $periodoApuracao ---');

    try {
      // Passo 1: Obter a guia DAS via API do SERPRO
      final pgmeiService = PgmeiService(_apiClient);
      
      print('1. Solicitando emissão de DAS no SERPRO...');
      final dasResponse = await pgmeiService.gerarDas(
        cnpjMei,
        periodoApuracao,
      );

      if (!dasResponse.sucesso || dasResponse.dados == null) {
        print('Erro no SERPRO: ${dasResponse.mensagemErro}');
        return false;
      }

      final dadosDas = dasResponse.dados!;
      print('DAS gerado com sucesso pelo SERPRO.');

      // Passo 2: Registrar o valor e a linha digitável na API do Questor
      print('2. Sincronizando com a API do Questor...');
      await _questorApi.registrarLancamentoTributario(
        cnpj: cnpjMei,
        periodo: periodoApuracao,
        valor: dadosDas.valorTotal,
        linhaDigitavel: dadosDas.linhaDigitavel,
      );

      // Passo 3: Enviar o documento PDF gerado para a API do Acessórias
      print('3. Enviando PDF do imposto para o Acessórias...');
      await _acessoriasApi.enviarGuiaAoCliente(
        cnpj: cnpjMei,
        nomeArquivo: 'DAS_MEI_$periodoApuracao.pdf',
        pdfBase64: dadosDas.pdf, // PDF codificado em Base64 vindo do SERPRO
      );

      print('--- Processamento concluído com sucesso! ---');
      return true;

    } catch (e) {
      print('Falha crítica na orquestração fiscal: $e');
      return false;
    }
  }
}
```

### Como executar esse fluxo em lote no seu ERP:

```dart
void executarRotinaFaturamento() async {
  // 1. Inicializar Clientes de API
  final serproClient = ApiClient();
  final questorApi = QuestorApi();
  final acessoriasApi = AcessoriasApi();

  // 2. Conectar Orquestrador
  final orquestrador = OrquestradorFiscal(
    apiClient: serproClient,
    questorApi: questorApi,
    acessoriasApi: acessoriasApi,
  );

  // 3. Rodar processamento para a carteira de clientes
  List<String> cnpjsClientes = ['00000000000000', '11111111111111'];
  String periodo = '202401';

  for (var cnpj in cnpjsClientes) {
    await orquestrador.processarFechamentoMensalMEI(cnpj, periodo);
  }
}
```
