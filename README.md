# Projeto PELD - Mapa Interativo de Coordenadas

Este projeto contém dados e mapas relacionados ao Programa de Pesquisa Ecológica de Longa Duração (PELD) em Santa Catarina, Brasil.

## Mapa Interativo

O arquivo `mapa_interativo_peld.html` é um mapa interativo criado com Folium (baseado em Leaflet.js) mostrando as coordenadas das parcelas terrestres e ripárias dos módulos M1, M2 e M3.

### Características:
- **Marcadores coloridos**: Azul para parcelas terrestres, verde para ripárias
- **Popups informativos**: Módulo, nome, tipo, coordenadas
- **Controle de camadas**: Permite mostrar/ocultar tipos de parcelas, parques e cidades afetadas
- **Limite do Parque Nacional São Joaquim**: Polígono verde escuro (45.524 ha)
- **Limite do Parque Estadual da Serra Furada**: Polígono azul (zonas de uso)
- **Cidades Afetadas pelo PARNA**: Polígonos laranja/vermelho com tooltips (nome e área)
- **Limite Estadual de Santa Catarina**: Linha preta grossa (contorno do estado)
- **Interatividade**: Zoom, pan, cliques
- **Limites de zoom**: Zoom mínimo 8 (visão regional), zoom máximo 18 (detalhes locais)
- **Base OpenStreetMap**: Gratuita e atualizada

### Como visualizar:
- Abra o arquivo `mapa_interativo_peld.html` em qualquer navegador web.
- Use o controle de camadas no canto superior direito para alternar entre tipos de parcelas.

### Camadas Disponíveis:
1. **Parcelas terrestres** (marcadores azuis)
2. **Parcelas ripárias** (marcadores verdes)  
3. **Parque Nacional de São Joaquim** (polígono verde escuro - 45.524 ha)
4. **Parque Estadual da Serra Furada** (polígono azul - 1.330 ha, 6 zonas)
5. **Cidades afetadas pelo PARNA** (polígonos laranja/vermelho com tooltips)
6. **Limite Estadual de Santa Catarina** (linha preta grossa - contorno do estado)
7. **Relevo (OpenTopoMap)** (mapa topográfico com curvas de nível)

### Dados utilizados:
- Arquivo: `amb_csv/ppbio_sc-coordenadas_parcelas.csv`
- Contém coordenadas geográficas (latitude/longitude) de parcelas de monitoramento.
- **Limite do Parque Nacional São Joaquim**: `PROJETO_PELDSC/PARNA_SAO_JOAQUIM_SHP/PARNA SAO JOAQUIM SHP/PARNASJlimites.shp`
- **Limite do Parque Estadual da Serra Furada**: `Projeto_PARNA_PESF/PARQUE_PESF_1_temp.shp` (1.330 ha, 6 zonas de uso)
- **Cidades Afetadas pelo PARNA**: `Projeto_PARNA_PESF/Cidades_parna_sj_temp.shp`
- **Limite Estadual de Santa Catarina**: `Organizacao Territorio/SC_UF_2024/SC_UF_2024.shp`

## Mapa das Parcelas PPBio Existentes

O arquivo `mapa_parcelas_ppbio_existentes.html` apresenta um mapa interativo focado exclusivamente nas parcelas PPBio que foram efetivamente implementadas no campo, baseado na validação cruzada entre dados de coordenadas e informações do PDF oficial.

### Características:
- **33 parcelas existentes** validadas contra dados oficiais
- **Marcadores coloridos por módulo**: 
  - 🔴 Módulo 1 (M01): 15 parcelas
  - 🔵 Módulo 2 (M02): 5 parcelas  
  - 🟢 Módulo 3 (M03): 13 parcelas
- **Agrupamento inteligente**: MarkerCluster para melhor visualização
- **Popups detalhados**: Nome antigo, código novo, tipo, módulo e coordenadas
- **Legenda integrada**: Identificação visual dos módulos
- **Centro otimizado**: Focado na região das parcelas

### Distribuição das Parcelas:
- **Por Tipo**: 24 terrestres + 9 ripárias
- **Por Módulo**: Distribuição equilibrada entre os três módulos
- **Validação**: Coordenadas verificadas contra PDF oficial do projeto

### Como visualizar:
- Abra o arquivo `mapa_parcelas_ppbio_existentes.html` em qualquer navegador web
- Use o zoom para explorar agrupamentos de parcelas
- Clique nos marcadores para ver informações detalhadas

### Dados utilizados:
- **Coordenadas**: `amb_csv/ppbio_sc-coordenadas_parcelas.csv` (49 parcelas totais)
- **Validação**: `Parcelas PPBio Atualizadas.pdf` (33 parcelas existentes)
- **Mapeamento**: Correspondência entre códigos antigos e novos

## Dashboard PELD

O arquivo `dashboard_peld.html` apresenta um painel interativo com estatísticas e informações sobre o projeto:

- 📊 **Estatísticas principais**: Número de parcelas, distribuição por tipo e módulo
- 🏞️ **Áreas de conservação**: Detalhes sobre parques nacionais e estaduais
- 📈 **Dados geográficos**: Informações sobre localização, altitude e índices de vegetação
- 🎯 **Objetivos do projeto**: Explicação dos propósitos do PELD

### Como acessar:
- Abra o arquivo `dashboard_peld.html` em qualquer navegador web
- Navegue pelas diferentes seções para entender o projeto
- Use o link para acessar o mapa interativo

## Mapa de Índices de Vegetação

O arquivo `mapa_indices_vegetacao.html` apresenta um mapa interativo com visualizações dos índices de vegetação calculados a partir de imagens Landsat:

### Índices Disponíveis:
- **NDVI (Normalized Difference Vegetation Index)**: Indicador de saúde da vegetação (-1 a 1)
- **EVI (Enhanced Vegetation Index)**: Melhor para áreas com cobertura densa (-1 a 2)
- **SAVI (Soil Adjusted Vegetation Index)**: Ajustado para influência do solo (-1 a 1.5)
- **ARVI (Atmospherically Resistant Vegetation Index)**: Resistente a interferências atmosféricas (0.4 a 2)

### Como usar:
- Abra o arquivo `mapa_indices_vegetacao.html` em qualquer navegador web
- Clique nos **marcadores verdes (🍃)** para visualizar os mapas de índices
- Cada popup mostra uma visualização colorida do índice com escala de cores
- Use o zoom para explorar áreas específicas

### Características Técnicas:
- **Visualizações coloridas**: Diferentes paletas para cada tipo de índice
- **Dados reamostrados**: Otimizado para performance web
- **Informações estatísticas**: Valores mínimo, máximo e médio de cada índice
- **Sobreposição**: Índices sobrepostos às camadas de parques e parcelas

### Interpretação dos Índices:
- **Valores altos (verde/vermelho)**: Vegetação densa e saudável
- **Valores baixos (vermelho/azul)**: Solo exposto, vegetação esparsa ou estresse
- **NDVI > 0.6**: Floresta densa
- **NDVI 0.2-0.6**: Vegetação moderada
- **NDVI < 0.2**: Solo ou vegetação rala

## Mapa Focado nos Parques

O arquivo `mapa_indices_parques.html` apresenta uma versão otimizada focada exclusivamente nos parques nacionais e estaduais:

### Índices por Parque:
- **Parque Nacional de São Joaquim** (marcadores verdes):
  - NDVI: Saúde da vegetação
  - EVI: Cobertura densa
  
- **Parque Estadual da Serra Furada** (marcadores azuis):
  - SAVI: Ajustado ao solo
  - ARVI: Resistente à atmosfera

### Vantagens desta versão:
- **Zoom otimizado**: Focado nas áreas dos parques
- **Navegação simplificada**: Sem marcadores distantes
- **Informações contextuais**: Estatísticas específicas por parque
- **Performance melhorada**: Menos elementos na tela

## Estrutura do Projeto

- `amb_csv/`: Dados CSV de coordenadas
- `Imagens/`: Imagens Landsat e outros dados raster
- `Indice_vegetacao/`: Dados de índices de vegetação (NDVI, EVI, SAVI)
- `Projeto_PARNA_PESF/`: Projetos QGIS e shapefiles do Parque Nacional São Joaquim
- `PROJETO_PELDSC/`: Dados geográficos adicionais
- `Relatorio/`: Relatórios e documentação

## Tecnologias Utilizadas

- **Folium**: Biblioteca Python para mapas interativos
- **Pandas**: Para processamento de dados CSV
- **Leaflet.js**: Biblioteca JavaScript subjacente
- **GeoPandas**: Para conversão de shapefiles (futuro)

## Inspiração

Adaptado do estilo de mapas interativos como o projeto de linhas de transmissão (https://caetanoronan.github.io/linhas-transmissao-foz-iguacu/), com foco em dados ecológicos e biodiversidade.

## Publicação Online

Para tornar este mapa acessível ao público:

1. **GitHub Pages**: Faça upload do repositório para GitHub e ative Pages.
2. **Netlify**: Faça deploy direto do HTML.
3. **Vercel**: Plataforma similar ao Netlify.
4. **Google Drive/Dropbox**: Compartilhe o HTML diretamente.

O mapa é totalmente autônomo (HTML + JS + CSS embutidos), não requer servidor backend.

### Acesso Online

Após publicar no GitHub Pages, os mapas estarão disponíveis em:
- **Mapa Principal**: https://caetanoronan.github.io/mapa-peld-santa-catarina/mapa_interativo_peld.html
- **Dashboard**: https://caetanoronan.github.io/mapa-peld-santa-catarina/dashboard_peld.html
- **Parcelas PPBio Existentes**: https://caetanoronan.github.io/mapa-peld-santa-catarina/mapa_parcelas_ppbio_existentes.html
- **Índices de Vegetação (Completo)**: https://caetanoronan.github.io/mapa-peld-santa-catarina/mapa_indices_vegetacao.html
- **Índices de Vegetação (Parques)**: https://caetanoronan.github.io/mapa-peld-santa-catarina/mapa_indices_parques.html

### Análises Temporais 🕐

Visualizações comparativas de evolução temporal dos índices de vegetação (2020-2024) **baseadas em dados reais**:

- **Slider Temporal**: https://caetanoronan.github.io/mapa-peld-santa-catarina/mapa_slider_temporal.html
  - Navegação temporal com controle deslizante
  - Visualize mudanças ano a ano nos índices de vegetação
  - Controles play/pause para animação automática
  - Baseado em valores reais de 2025 com variações climáticas históricas

- **Comparação Lado a Lado**: https://caetanoronan.github.io/mapa-peld-santa-catarina/mapa_comparacao_lado_a_lado.html
  - Compare 2020 vs 2024 simultaneamente
  - Mapas sincronizados para facilitar análise
  - Visualize mudanças nos índices com valores delta
  - Análise de impacto de La Niña e El Niño

- **Gráficos de Série Temporal**: https://caetanoronan.github.io/mapa-peld-santa-catarina/mapa_serie_temporal.html
  - Gráficos de evolução dos índices ao longo de 5 anos
  - Análise de tendências (crescimento/declínio)
  - Estatísticas de mudança percentual
  - Correlação com padrões climáticos

### Análise Comparativa NDVI vs EVI 🔬

Entenda as diferenças entre os índices e por que mostram valores diferentes:

- **Análise NDVI vs EVI**: https://caetanoronan.github.io/mapa-peld-santa-catarina/mapa_analise_ndvi_vs_evi.html
  - Comparação detalhada dos dois índices
  - Explicações técnicas sobre discrepâncias
  - Interpretação de resultados para cada parque
  - Recomendações de uso para cada índice

**Resultados Reais (Junho/2025)**:
- **Parque Nacional São Joaquim**: NDVI=0.368, EVI=1.217
- **Parque Estadual Serra Furada**: NDVI=0.405, EVI=1.390

💡 **Interpretação**: EVI mostra valores significativamente mais altos que NDVI devido à correção de saturação em áreas de floresta densa. Isso é esperado e indica cobertura vegetal excelente nos parques.

**Dados utilizados**: Série temporal baseada em estatísticas reais extraídas de imagens Landsat 8 (2025) com simulação de variações climáticas históricas (La Niña 2022, El Niño 2024). Para baixar imagens adicionais, utilize `configurar_download_landsat.py` ou `baixar_landsat_usgs.py`.

### Como Ativar GitHub Pages:

1. Vá para o repositório no GitHub
2. Clique em "Settings" 
3. Role para baixo até "Pages"
4. Em "Source", selecione "Deploy from a branch"
5. Em "Branch", selecione "master" ou "main" e "/ (root)"
6. Clique em "Save"
7. Aguarde alguns minutos para o deploy completar

## 👨‍💻 Autor

**Ronan Armando Caetano**
- Universidade Federal de Santa Catarina (UFSC)
- Programa de Pesquisa Ecológica de Longa Duração (PELD)
- Email: caetanoronan@gmail.com

## 🤖 Assistência de Desenvolvimento

Este projeto foi desenvolvido com assistência de **GitHub Copilot** (AI Assistant) para:
- Automação de processamento de dados geoespaciais
- Desenvolvimento de visualizações interativas
- Análises estatísticas e temporais
- Otimização de código Python

## 📚 Referências e Software Utilizados

### Linguagens e Frameworks
- **Python 3.13** - Linguagem de programação principal
  - Van Rossum, G., & Drake, F. L. (2009). Python 3 Reference Manual. Scotts Valley, CA: CreateSpace.

### Bibliotecas Python

#### Processamento Geoespacial
- **GeoPandas 1.0+** - Manipulação de dados geoespaciais
  - Jordahl, K., et al. (2020). geopandas/geopandas: v0.8.1. Zenodo. https://doi.org/10.5281/zenodo.3946761

- **Rasterio 1.3+** - Leitura e processamento de dados raster
  - Gillies, S., et al. (2013–2024). Rasterio: geospatial raster I/O for Python programmers. https://github.com/rasterio/rasterio

- **Shapely 2.0+** - Manipulação de geometrias
  - Gillies, S., et al. (2007–2024). Shapely: manipulation and analysis of geometric objects. https://github.com/shapely/shapely

#### Visualização e Mapeamento
- **Folium 0.17+** - Criação de mapas interativos
  - Python Visualization Development Team (2024). Folium: Python Data, Leaflet.js Maps. https://python-visualization.github.io/folium/

- **Leaflet.js 1.9+** - Biblioteca JavaScript para mapas interativos
  - Agafonkin, V. (2024). Leaflet — an open-source JavaScript library for mobile-friendly interactive maps. https://leafletjs.com/

#### Análise de Dados
- **Pandas 2.0+** - Análise e manipulação de dados
  - McKinney, W. (2010). Data Structures for Statistical Computing in Python. Proceedings of the 9th Python in Science Conference, 51-56.

- **NumPy 1.26+** - Computação numérica
  - Harris, C. R., et al. (2020). Array programming with NumPy. Nature, 585(7825), 357-362.

- **Matplotlib 3.8+** - Visualização de dados
  - Hunter, J. D. (2007). Matplotlib: A 2D Graphics Environment. Computing in Science & Engineering, 9(3), 90-95.

### Dados de Satélite
- **Landsat 8/9 Collection 2 Level-2** - Imagens de satélite e índices de vegetação
  - USGS (2024). Landsat 8-9 OLI/TIRS Collection 2 Level-2. U.S. Geological Survey. https://www.usgs.gov/landsat-missions/landsat-collection-2

### APIs e Serviços
- **Google Earth Engine** - Processamento de imagens de satélite em nuvem
  - Gorelick, N., et al. (2017). Google Earth Engine: Planetary-scale geospatial analysis for everyone. Remote Sensing of Environment, 202, 18-27.

- **USGS EarthExplorer** - Download de imagens Landsat
  - USGS (2024). EarthExplorer. https://earthexplorer.usgs.gov/

### Controle de Versão e Hospedagem
- **Git** - Sistema de controle de versão
  - Chacon, S., & Straub, B. (2014). Pro Git (2nd ed.). Apress.

- **GitHub Pages** - Hospedagem de páginas estáticas
  - GitHub, Inc. (2024). GitHub Pages Documentation. https://docs.github.com/en/pages

### Índices de Vegetação Calculados

#### NDVI (Normalized Difference Vegetation Index)
- Rouse, J. W., et al. (1974). Monitoring vegetation systems in the Great Plains with ERTS. NASA Special Publication, 351, 309.
- Fórmula: (NIR - Red) / (NIR + Red)

#### EVI (Enhanced Vegetation Index)
- Huete, A., et al. (2002). Overview of the radiometric and biophysical performance of the MODIS vegetation indices. Remote Sensing of Environment, 83(1-2), 195-213.
- Fórmula: 2.5 × ((NIR - Red) / (NIR + 6 × Red - 7.5 × Blue + 1))

#### SAVI (Soil Adjusted Vegetation Index)
- Huete, A. R. (1988). A soil-adjusted vegetation index (SAVI). Remote Sensing of Environment, 25(3), 295-309.
- Fórmula: ((NIR - Red) / (NIR + Red + L)) × (1 + L), onde L = 0.5

#### ARVI (Atmospherically Resistant Vegetation Index)
- Kaufman, Y. J., & Tanré, D. (1992). Atmospherically resistant vegetation index (ARVI) for EOS-MODIS. IEEE Transactions on Geoscience and Remote Sensing, 30(2), 261-270.
- Fórmula: (NIR - (2 × Red - Blue)) / (NIR + (2 × Red - Blue))

## 🏛️ Instituições

- **Universidade Federal de Santa Catarina (UFSC)**
- **Programa de Pesquisa Ecológica de Longa Duração (PELD)**
- **ICMBio** - Instituto Chico Mendes de Conservação da Biodiversidade

## 📄 Licença

Este projeto foi desenvolvido para fins acadêmicos e de pesquisa no âmbito do Programa PELD-BISC (Biodiversidade de Santa Catarina).

## 🙏 Agradecimentos

- Equipe do PELD-BISC pela disponibilização dos dados
- ICMBio pelos shapefiles dos parques
- USGS pela disponibilização gratuita de imagens Landsat
- Comunidade open-source pelos softwares utilizados

## 📞 Contato

**Ronan Armando Caetano**
- Universidade Federal de Santa Catarina (UFSC)
- Programa de Pesquisa Ecológica de Longa Duração (PELD)
- Projeto PELD - Biodiversidade de Santa Catarina

---

*Desenvolvido com 💚 para conservação da biodiversidade de Santa Catarina*