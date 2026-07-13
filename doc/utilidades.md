# Utilidades e Recursos da API SERPRO Integra Contador

Esta documentação descreve os principais recursos, serviços e automações que podem ser realizados utilizando este pacote de integração com a API do SERPRO Integra Contador.

---

## 1. Gestão de MEI (Microempreendedor Individual)

* **CCMEI (Cadastro Centralizado de MEI)**:
  * Consulta cadastral completa (nome empresarial, CPF, capital social, enquadramento e CNAEs).
  * Emissão do Certificado da Condição de Microempreendedor Individual (CCMEI) oficial em formato PDF.
  * Consulta de situação cadastral e histórico de vínculos por CPF.
* **PGMEI (Programa de Geração do DAS para o MEI)**:
  * Consulta de débitos e geração da guia de pagamento mensal DAS-MEI.
  * Emissão com código de barras.
  * Consulta de situação de dívida ativa.
  * Atualização de benefícios previdenciários.

---

## 2. Declarações e Obrigações Fiscais (Simples Nacional e Geral)

* **PGDAS-D (Programa Gerador do Documento de Arrecadação do Simples Nacional)**:
  * Transmissão mensal e anual de informações socioeconômicas e fiscais.
  * Cálculo de impostos devidos do Simples Nacional.
  * Geração mensal e avulsa do DAS.
  * Consulta a histórico de declarações transmitidas e extratos de pagamentos.
* **DEFIS (Declaração de Informações Socioeconômicas e Fiscais)**:
  * Transmissão e consulta de declarações DEFIS.
* **DCTFWeb**:
  * Transmissão da DCTFWeb (Previdenciário e Fundos).
  * Emissão de guias DARF.
  * Download e consulta de arquivos XML das declarações transmitidas.

---

## 3. Parcelamentos de Débitos (Simples Nacional e MEI)

Gerenciamento completo das seguintes modalidades de parcelamento:
* **PARCMEI** (MEI Ordinário) e **PARCMEI Especial**
* **PARCSN** (Simples Nacional Ordinário) e **PARCSN Especial**
* **PERTMEI** e **PERTSN** (Programa Especial de Regularização Tributária)
* **RELPMEI** e **RELPSN** (Programa de Reescalonamento de Débitos)

**Ações possíveis:**
* Solicitar novos pedidos de parcelamento.
* Consultar detalhes de pedidos ativos, parcelas pagas, saldos e composição de débitos.
* Emitir guias DAS de parcelamento atualizadas mensalmente.

---

## 4. Comunicação e e-CAC

* **Caixa Postal da Receita Federal**:
  * Consulta e monitoramento de alertas e comunicados oficiais enviados para a empresa (e-CAC).
  * Leitura e download de mensagens específicas.
* **DTE (Domicílio Tributário Eletrônico)**:
  * Verificação se o DTE está ativo para o contribuinte.
  * Recepção de intimações eletrônicas em lote.

---

## 5. Emissão de DARF e Cálculos (SICALC)

* **SICALC Web**:
  * Consolidação e cálculo de juros e multas para impostos federais vencidos.
  * Geração das guias de DARF atualizadas para pagamento.

---

## 6. Autenticação e Procurações Eletrônicas

* **Procurações**:
  * Consulta e verificação de vigência de procurações eletrônicas cadastradas para o e-CAC.
* **Autentica Procurador**:
  * Assinatura digital local de termos de procuração em XML utilizando certificado digital ICP-Brasil.
  * Obtenção e renovação automática de tokens para realizar operações em nome de clientes terceiros (Pessoa Física ou Jurídica).

---

## 7. Cadastro e Eventos

* **Eventos de Atualização**:
  * Monitoramento e captura de eventos de alteração cadastral em lotes para CPFs e CNPJs.
* **MIT (Manifesto de Importação de Trânsito)**:
  * Emissão e acompanhamento de trânsitos aduaneiros de importação.
