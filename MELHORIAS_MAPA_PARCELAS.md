# 🎉 Melhorias Implementadas no Mapa de Parcelas PPBio

**Data:** 10 de novembro de 2025  
**Arquivo:** `mapa_parcelas_ppbio.html`

---

## ✅ Alterações Realizadas

### 1. 🔍 **Controles de Zoom**
- ✅ **Zoom mínimo:** 8 (visão regional ampla)
- ✅ **Zoom máximo:** 18 (visão detalhada)
- ✅ **Zoom inicial:** 10 (visão equilibrada)

**Benefício:** Evita que usuários se percam navegando muito longe ou tenham dificuldade de ver detalhes.

---

### 2. 🗺️ **Limite Estadual de Santa Catarina**
- ✅ Adicionado contorno do estado de SC
- ✅ Estilo: Linha tracejada escura (`#2c3e50`)
- ✅ Transparente (sem preenchimento)
- ✅ Peso da linha: 3px
- ✅ Padrão: Traços de 5px com 5px de espaço
- ✅ Tooltip: "Santa Catarina"

**Fonte de dados:** `Organizacao Territorio/SC_UF_2024/SC_UF_2024.shp`

**Benefício:** Contexto geográfico estadual para localizar as parcelas.

---

### 3. 🏘️ **Limites Municipais (Cidades Atingidas pelo PARNA)**
- ✅ Adicionados polígonos dos municípios afetados pelo PARNA São Joaquim
- ✅ Preenchimento: Cinza claro (`#ecf0f1`) com 20% de opacidade
- ✅ Contorno: Cinza médio (`#95a5a6`)
- ✅ Peso da linha: 2px
- ✅ Tooltip com nome do município (campo `NM_MUN`)

**Municípios incluídos:**
1. Lauro Müller
2. Orleans
3. Urubici
4. Bom Jardim da Serra
5. Grão-Pará

**Fonte de dados:** `Projeto_PARNA_PESF/Cidades_parna_sj_temp.shp`

**Benefício:** Visualizar quais municípios são impactados pelo parque e onde estão as parcelas em relação aos limites administrativos.

---

### 4. 📊 **Legenda Atualizada**
- ✅ Seção "Parcelas" com cores:
  - 🟢 Verde: Instalada (PPBio Oficial)
  - 🟠 Laranja: Não Instalada (PPBio Oficial)
  - 🔵 Azul: Complementar (Coordenadas)

- ✅ **Nova seção "Limites Territoriais"** com:
  - Linha tracejada: Limite Estadual (SC)
  - Linha sólida cinza: Municípios PARNA

- ✅ Informações adicionais:
  - Total de parcelas: 51
  - Tipo (T = Terrestre | R = Ripária)
  - Limites de zoom (8 min - 18 max)

**Benefício:** Usuários entendem imediatamente o que cada elemento visual representa.

---

### 5. 🎛️ **Controle de Camadas Aprimorado**
- ✅ Controle expandido por padrão (`collapsed=False`)
- ✅ Camadas disponíveis para ligar/desligar:
  - OpenStreetMap (base padrão)
  - Satélite (Esri.WorldImagery)
  - Limite Estadual (SC)
  - Municípios Atingidos pelo PARNA
  - Módulo 01 (parcelas)
  - Módulo 02 (parcelas)
  - Módulo 03 (parcelas)

**Benefício:** Flexibilidade para visualizar apenas as informações desejadas.

---

## 📁 Arquivos Modificados

### Script Python
**Arquivo:** `gerar_mapa_parcelas.py`

**Mudanças principais:**
```python
# Importações adicionadas
import geopandas as gpd

# Configuração de zoom
m = folium.Map(
    location=[-28.133, -49.510],
    zoom_start=10,
    min_zoom=8,      # NOVO
    max_zoom=18,     # NOVO
    tiles='OpenStreetMap'
)

# Carregamento de shapefiles (NOVO)
SC_UF_SHP = BASE_DIR / "Organizacao Territorio/SC_UF_2024/SC_UF_2024.shp"
CIDADES_PARNA_SHP = BASE_DIR / "Projeto_PARNA_PESF/Cidades_parna_sj_temp.shp"

# Adição de camadas GeoJSON (NOVO)
- Limite estadual com estilo tracejado
- Municípios com tooltip de nome
```

### Mapa HTML Gerado
**Arquivo:** `mapa_parcelas_ppbio.html`

**Características:**
- 2.785 linhas de código
- 51 parcelas plotadas
- 2 camadas de limites territoriais
- 3 camadas de parcelas por módulo
- Legenda completa e interativa
- Controle de camadas expandido

---

## 🎯 Resumo Visual das Camadas

| Camada | Cor/Estilo | Opacidade | Tooltip | Controle |
|--------|-----------|-----------|---------|----------|
| **Limite SC** | Linha tracejada escura | 0% | "Santa Catarina" | ✅ |
| **Municípios PARNA** | Cinza claro | 20% | Nome do município | ✅ |
| **Parcelas Instaladas** | Verde | 60% | Detalhes completos | ✅ |
| **Parcelas Não Instaladas** | Laranja | 60% | Detalhes completos | ✅ |
| **Parcelas Complementares** | Azul | 60% | Detalhes completos | ✅ |

---

## 📊 Estatísticas Finais

### Parcelas por Módulo
- **M01:** 15 parcelas
- **M02:** 21 parcelas
- **M03:** 15 parcelas
- **Total:** 51 parcelas

### Parcelas por Origem
- **PPBio Oficial:** Dados do PDF (instaladas e não instaladas)
- **Complementares:** Do arquivo de coordenadas (códigos T1-T10, R1-R3, *_RIP*, *_PSA*)

### Limites Territoriais
- **1** limite estadual (Santa Catarina)
- **5** municípios atingidos pelo PARNA

---

## 🚀 Como Usar

### Para visualizar:
1. Abra `mapa_parcelas_ppbio.html` no navegador
2. Use o controle de camadas (canto superior direito) para ligar/desligar elementos
3. Clique nos marcadores para ver detalhes de cada parcela
4. Passe o mouse sobre os limites municipais para ver o nome da cidade

### Para zoom:
- **Scroll do mouse** ou **botões +/-** para ampliar/reduzir
- Limite mínimo (8) mostra contexto regional
- Limite máximo (18) permite ver detalhes precisos

### Para alternar camadas base:
- Escolha entre **OpenStreetMap** (padrão) ou **Satélite** (Esri)
- Útil para ver vegetação real vs. mapa de ruas

---

## 🔧 Comandos para Regenerar o Mapa

Se precisar atualizar o mapa após modificar os dados:

```powershell
# Ativar ambiente virtual (se necessário)
.\.venv\Scripts\Activate.ps1

# Executar script de geração
python gerar_mapa_parcelas.py
```

**Saída esperada:**
```
Mapa gerado: c:\Users\...\mapa_parcelas_ppbio.html
Total de parcelas plotadas: 51
  • PPBio Oficial: XX
  • Complementares: XX
  • Instaladas: XX

Abra o arquivo em um navegador para visualizar!
```

---

## 💡 Próximas Melhorias Sugeridas (Futuro)

- [ ] Adicionar limite do PARNA São Joaquim (shapefile já existe)
- [ ] Incluir curvas de nível para análise topográfica
- [ ] Adicionar rios principais da região
- [ ] Criar filtro dinâmico por tipo (T/R) e status (instalada/não)
- [ ] Exportar dados filtrados para CSV diretamente do mapa
- [ ] Adicionar medição de distância entre parcelas
- [ ] Incluir fotos/imagens das parcelas instaladas (se disponíveis)

---

## 📚 Referências Técnicas

### Bibliotecas Utilizadas
- **Folium:** Geração de mapas Leaflet em Python
- **GeoPandas:** Manipulação de dados geoespaciais
- **GeoJSON:** Formato de dados geográficos

### Sistemas de Coordenadas
- **EPSG:4326** (WGS84) - Latitude/Longitude
- Parcelas e limites projetados automaticamente

### Fontes de Dados
- Parcelas: `amb_csv/ppbio_parcelas_atualizadas.geojson`
- Limite SC: `Organizacao Territorio/SC_UF_2024/`
- Municípios: `Projeto_PARNA_PESF/Cidades_parna_sj_temp.shp`

---

**Desenvolvido por:** Ronan Armando Caetano (UFSC)  
**Com assistência de:** GitHub Copilot  
**Projeto:** PELD-BISC 2025  
**Última atualização:** 10 de novembro de 2025
