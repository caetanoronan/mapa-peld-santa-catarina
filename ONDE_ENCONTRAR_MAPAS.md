# 🗺️ Guia de Acesso aos Mapas e Dados PELD

## 📊 Dashboard Principal
**Arquivo:** `dashboard_peld.html`  
**Descrição:** Dashboard centralizado com links para todos os mapas, estatísticas e controles interativos.  
**Novo:** Agora com toggle para alternar entre parcelas oficiais (31) e gerais (57, incluindo complementares).

---

## 🗺️ Mapas Interativos Disponíveis

### 1. Mapa Principal PELD
**Arquivo:** `mapa_interativo_peld.html`  
**Conteúdo:** Todas as parcelas originais, parques, cidades e camadas topográficas  
**Características:** Controle de camadas completo, popups informativos

### 2. Mapa de Parcelas PPBio (ATUALIZADO v2.0! ✨)
**Arquivo:** `mapa_parcelas_ppbio.html`  
**Conteúdo:** 51 parcelas com coordenadas espaciais (23 oficiais + 28 complementares)  
**Características:**
- ✅ Verde: Instaladas (PPBio Oficial)
- 🟠 Laranja: Não instaladas (PPBio Oficial)
- 🔵 Azul: Complementares (do arquivo de coordenadas)
- Controle por módulo (M01, M02, M03)
- Popups detalhados com origem, tipo (T/R), status
- **🆕 PARNA São Joaquim** (polígono verde semi-transparente) 🏞️
- **🆕 Limite estadual de SC** (linha tracejada)
- **🆕 Limites municipais** das cidades atingidas pelo PARNA (5 municípios)
- **🆕 Controles de zoom FUNCIONANDO:** mín 8, máx 18 ✅
- **🆕 Escala** visível no mapa
- Camadas base: OpenStreetMap + Satélite (Esri)
- Legenda completa e controle de 8 camadas expandido

### 3. Índices de Vegetação
**Arquivo:** `mapa_indices_parques.html`  
**Conteúdo:** NDVI, EVI, SAVI, ARVI dos parques

### 4. Análise Temporal - Slider
**Arquivo:** `mapa_slider_temporal.html`  
**Conteúdo:** Navegação temporal 2020-2024 com controle deslizante

### 5. Comparação Lado a Lado
**Arquivo:** `mapa_comparacao_lado_a_lado.html`  
**Conteúdo:** 2020 vs 2024 sincronizados

### 6. Série Temporal com Gráficos
**Arquivo:** `mapa_serie_temporal.html`  
**Conteúdo:** Evolução dos índices em gráficos

### 7. Análise NDVI vs EVI
**Arquivo:** `mapa_analise_ndvi_vs_evi.html`  
**Conteúdo:** Comparação técnica dos índices

---

## 📁 Arquivos de Dados das Parcelas

### Tabelas CSV/XLSX

#### Oficiais (PPBio PDF)
- `amb_csv/ppbio_parcelas_atualizadas.csv` (31 linhas - básico: antigo, novo, existência)
- `amb_csv/ppbio_parcelas_atualizadas_completo.csv` (57 linhas - com complementares)
- `amb_csv/ppbio_parcelas_atualizadas.xlsx` (Excel multi-sheet)
  - Aba: **Geral** → 57 parcelas (oficiais + complementares)
  - Aba: **Resumo_oficial** → Resumo de 31 parcelas PPBio
  - Aba: **Resumo_geral** → Resumo de 57 parcelas (todos)

#### Resumos
- `amb_csv/ppbio_parcelas_resumo_modulos.csv` → Resumo oficial (31 parcelas)
  - M01: 15 (100% instaladas)
  - M02: 14 (28.6% instaladas)
  - M03: 2 (0% instaladas)
  - TOTAL: 31 (19 instaladas, 61.3%)

- `amb_csv/ppbio_parcelas_resumo_modulos_geral.csv` → Resumo geral (57 parcelas)
  - M01: 15 (100% instaladas)
  - M02: 27 (14.8% instaladas)
  - M03: 15 (0% instaladas)
  - TOTAL: 57 (19 instaladas, 33.3%)

#### Por Módulo
Diretório: `amb_csv/parcelas_por_modulo/`
- `parcelas_M01.csv` / `parcelas_M01.xlsx`
- `parcelas_M02.csv` / `parcelas_M02.xlsx`
- `parcelas_M03.csv` / `parcelas_M03.xlsx`

### Dados Espaciais

- `amb_csv/ppbio_parcelas_atualizadas.geojson` → GeoJSON com 51 features (geometrias Point)
- `amb_csv/ppbio_parcelas_atualizadas_map.csv` → CSV com coordenadas (51 linhas)
- `amb_csv/ppbio_sc-coordenadas_parcelas.csv` → Coordenadas originais (49 linhas)

---

## 🔍 Entendendo a Estrutura dos Dados

### Colunas Principais

**Dados Oficiais (de PDF):**
- `antigo`: Código antigo PPBio (ex: TN0500M01T01)
- `novo`: Código novo simplificado (ex: T01)
- `existencia`: SIM, NÃO ou DESCONHECIDA
- `modulo`: M01, M02, M03
- `tipo_parcela`: T (Terrestre) ou R (Ripária)
- `instalada`: True/False

**Metadados de Integração (NOVO):**
- `origem`: "PPBio_oficial" ou "Complementar_local"
- `padrao_ppbio`: True se segue padrão oficial, False se complementar
- `codigo_bruto`: Nome original no arquivo de coordenadas (ex: TL054_RIP8, T1, R3)
- `base_ppbio`: Código base normalizado (ex: TL054, TW065, T1)

### Parcelas Complementares

São parcelas presentes no arquivo de coordenadas (`ppbio_sc-coordenadas_parcelas.csv`) mas não no PDF oficial:

**Módulo M02 (13 complementares):**
- Ripárias com sufixos: TL054_RIP8, TL077_RIP7, TL4200_RIP, etc.
- PSA: RIP_PSA3, RIP_PSA8, TL3500_PSA2, TL4500_PSA1
- Terrestres: TL400_PSA4

**Módulo M03 (13 complementares):**
- Terrestres: T1, T2, T3, T4, T5, T6, T7, T8, T9, T10
- Ripárias: R1, R2, R3

---

## 🚀 Como Usar

### Para visualizar os mapas:
1. Abra `dashboard_peld.html` no navegador (ponto de entrada principal)
2. Ou abra diretamente qualquer `mapa_*.html`

### Para explorar as parcelas especificamente:
1. **Mapa visual:** Abra `mapa_parcelas_ppbio.html`
2. **Dashboard com estatísticas:** Abra `dashboard_peld.html` e ative o toggle "Incluir parcelas complementares"

### Para análise de dados:
1. **Excel:** Abra `amb_csv/ppbio_parcelas_atualizadas.xlsx`
2. **CSV:** Qualquer arquivo em `amb_csv/` pode ser importado em Python/R/QGIS
3. **GIS:** Carregue `ppbio_parcelas_atualizadas.geojson` em QGIS/ArcGIS

---

## 📍 Localização dos Arquivos

```
c:\Users\caetanoronan\OneDrive - UFSC\Documentos\PELD -\
├── dashboard_peld.html                    ← DASHBOARD PRINCIPAL
├── mapa_parcelas_ppbio.html               ← NOVO MAPA DE PARCELAS
├── mapa_interativo_peld.html              ← Mapa original
├── mapa_indices_parques.html
├── mapa_slider_temporal.html
├── mapa_comparacao_lado_a_lado.html
├── mapa_serie_temporal.html
├── mapa_analise_ndvi_vs_evi.html
│
└── amb_csv/
    ├── ppbio_parcelas_atualizadas.csv
    ├── ppbio_parcelas_atualizadas_completo.csv
    ├── ppbio_parcelas_atualizadas.xlsx
    ├── ppbio_parcelas_resumo_modulos.csv
    ├── ppbio_parcelas_resumo_modulos_geral.csv
    ├── ppbio_parcelas_atualizadas.geojson
    ├── ppbio_parcelas_atualizadas_map.csv
    ├── ppbio_sc-coordenadas_parcelas.csv
    └── parcelas_por_modulo/
        ├── parcelas_M01.csv
        ├── parcelas_M01.xlsx
        ├── parcelas_M02.csv
        ├── parcelas_M02.xlsx
        ├── parcelas_M03.csv
        └── parcelas_M03.xlsx
```

---

## ✅ Resumo Rápido

| Tipo | Arquivo Principal | O que Mostra |
|------|------------------|--------------|
| 🎯 **Início** | `dashboard_peld.html` | Todos os mapas + estatísticas dinâmicas |
| 🗺️ **Parcelas** | `mapa_parcelas_ppbio.html` | 51 parcelas (oficiais + complementares) |
| 📊 **Dados** | `ppbio_parcelas_atualizadas.xlsx` | Planilha completa com 3 abas |
| 🌍 **GIS** | `ppbio_parcelas_atualizadas.geojson` | Dados espaciais para SIG |

---

**Desenvolvido por:** Ronan Armando Caetano (UFSC)  
**Com assistência de:** GitHub Copilot — Raptor mini (Preview)  
**Projeto:** PELD-BISC 2025
