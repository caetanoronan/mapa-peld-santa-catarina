# 📜 Créditos e Referências
## Projeto PELD - Mapas Interativos de Santa Catarina

---

## 👨‍💻 AUTOR

**Ronan Armando Caetano**
- **Instituição:** Universidade Federal de Santa Catarina (UFSC)
- **Programa:** Pesquisa Ecológica de Longa Duração (PELD)
- **Projeto:** PELD-BISC - Biodiversidade de Santa Catarina
- **Ano:** 2025
- **Funções e Formação:**
  - Graduando em Ciências Biológicas — UFSC
  - Técnico em Geoprocessamento — IFSC
  - Técnico em Saneamento (curso técnico)

---

- ## 🤖 ASSISTÊNCIA DE DESENVOLVIMENTO

Este projeto recebeu assistência de **GitHub Copilot** (AI assistant). A versão do modelo utilizada foi **Raptor mini (Preview)**.

**Contribuições da IA:**
- Automação de processamento de dados geoespaciais em Python
- Desenvolvimento de visualizações interativas com Folium/Leaflet
- Criação de análises estatísticas e temporais
- Implementação de comparações entre índices de vegetação
- Otimização de código e debugging
- Documentação técnica e comentários
- Integração com APIs e serviços de dados satelitais

---

## 📚 SOFTWARE E BIBLIOTECAS UTILIZADAS

### Linguagem de Programação
- **Python 3.13.0**
  - Van Rossum, G., & Drake, F. L. (2009). *Python 3 Reference Manual*. Scotts Valley, CA: CreateSpace.
  - https://www.python.org/

### Processamento Geoespacial

#### GeoPandas 1.0.1
- **Descrição:** Extensão do Pandas para dados geoespaciais
- **Referência:** Jordahl, K., Van den Bossche, J., Fleischmann, M., Wasserman, J., McBride, J., Gerard, J., ... & Leblanc, F. (2020). *geopandas/geopandas: v0.8.1* (Version v0.8.1). Zenodo. https://doi.org/10.5281/zenodo.3946761
- **Uso no projeto:** Manipulação de shapefiles dos parques e limites territoriais

#### Rasterio 1.3.10
- **Descrição:** Leitura e escrita de dados geoespaciais raster
- **Referência:** Gillies, S., et al. (2013–2024). *Rasterio: geospatial raster I/O for Python programmers*. https://github.com/rasterio/rasterio
- **Uso no projeto:** Processamento de imagens Landsat e cálculo de índices de vegetação

#### Shapely 2.0.6
- **Descrição:** Manipulação e análise de objetos geométricos
- **Referência:** Gillies, S., et al. (2007–2024). *Shapely: manipulation and analysis of geometric objects*. https://github.com/shapely/shapely
- **Uso no projeto:** Operações geométricas e cálculo de centroides

### Visualização e Mapeamento

#### Folium 0.17.0
- **Descrição:** Criação de mapas interativos baseados em Leaflet.js
- **Referência:** Python Visualization Development Team (2024). *Folium: Python Data, Leaflet.js Maps*. https://python-visualization.github.io/folium/
- **Uso no projeto:** Geração de todos os 7 mapas interativos

#### Leaflet.js 1.9.4
- **Descrição:** Biblioteca JavaScript para mapas interativos mobile-friendly
- **Referência:** Agafonkin, V. (2024). *Leaflet — an open-source JavaScript library for mobile-friendly interactive maps*. https://leafletjs.com/
- **Uso no projeto:** Base JavaScript para todos os mapas interativos

### Análise de Dados

#### Pandas 2.2.3
- **Descrição:** Estruturas de dados e análise
- **Referência:** McKinney, W. (2010). Data Structures for Statistical Computing in Python. *Proceedings of the 9th Python in Science Conference*, 51-56. https://doi.org/10.25080/Majora-92bf1922-00a
- **Uso no projeto:** Processamento de CSV com coordenadas das parcelas

#### NumPy 2.2.1
- **Descrição:** Computação numérica e arrays multidimensionais
- **Referência:** Harris, C. R., Millman, K. J., van der Walt, S. J., et al. (2020). Array programming with NumPy. *Nature*, 585(7825), 357-362. https://doi.org/10.1038/s41586-020-2649-2
- **Uso no projeto:** Cálculos matriciais de índices de vegetação

#### Matplotlib 3.9.3
- **Descrição:** Biblioteca de visualização 2D
- **Referência:** Hunter, J. D. (2007). Matplotlib: A 2D Graphics Environment. *Computing in Science & Engineering*, 9(3), 90-95. https://doi.org/10.1109/MCSE.2007.55
- **Uso no projeto:** Geração de gráficos auxiliares e visualizações

---

## 🛰️ DADOS DE SATÉLITE

### Landsat 8/9 Collection 2 Level-2
- **Fonte:** U.S. Geological Survey (USGS)
- **Referência:** USGS (2024). *Landsat 8-9 OLI/TIRS Collection 2 Level-2*. U.S. Geological Survey. https://www.usgs.gov/landsat-missions/landsat-collection-2
- **Uso no projeto:** 
  - Imagens de junho/2025 para cálculo de índices de vegetação
  - Bandas espectrais: Blue (B2), Green (B3), Red (B4), NIR (B5), SWIR (B6)
- **Resolução Espacial:** 30 metros
- **Resolução Temporal:** 16 dias (Landsat 8/9 combinados: 8 dias)

---

## 🌍 SERVIÇOS E APIs

### Google Earth Engine
- **Descrição:** Plataforma de processamento geoespacial em nuvem
- **Referência:** Gorelick, N., Hancher, M., Dixon, M., Ilyushchenko, S., Thau, D., & Moore, R. (2017). Google Earth Engine: Planetary-scale geospatial analysis for everyone. *Remote Sensing of Environment*, 202, 18-27. https://doi.org/10.1016/j.rse.2017.06.031
- **Uso no projeto:** Scripts preparados para download de séries temporais

### USGS EarthExplorer
- **Fonte:** U.S. Geological Survey
- **Referência:** USGS (2024). *EarthExplorer*. https://earthexplorer.usgs.gov/
- **Uso no projeto:** Download de imagens Landsat históricas

### OpenStreetMap
- **Referência:** OpenStreetMap contributors (2024). *OpenStreetMap*. https://www.openstreetmap.org/
- **Uso no projeto:** Camada base dos mapas interativos

### OpenTopoMap
- **Referência:** OpenTopoMap (2024). *OpenTopoMap - Topographic map from OpenStreetMap data*. https://opentopomap.org/
- **Uso no projeto:** Camada topográfica com curvas de nível

---

## 📊 ÍNDICES DE VEGETAÇÃO - REFERÊNCIAS CIENTÍFICAS

### NDVI (Normalized Difference Vegetation Index)
- **Referência Original:** Rouse, J. W., Haas, R. H., Schell, J. A., & Deering, D. W. (1974). Monitoring vegetation systems in the Great Plains with ERTS. *NASA Special Publication*, 351, 309.
- **Fórmula:** NDVI = (NIR - Red) / (NIR + Red)
- **Faixa de valores:** -1 a +1
- **Interpretação:**
  - > 0.7: Vegetação densa e saudável
  - 0.4 - 0.7: Vegetação moderada
  - < 0.4: Solo exposto ou vegetação esparsa

### EVI (Enhanced Vegetation Index)
- **Referência Original:** Huete, A., Didan, K., Miura, T., Rodriguez, E. P., Gao, X., & Ferreira, L. G. (2002). Overview of the radiometric and biophysical performance of the MODIS vegetation indices. *Remote Sensing of Environment*, 83(1-2), 195-213. https://doi.org/10.1016/S0034-4257(02)00096-2
- **Fórmula:** EVI = 2.5 × ((NIR - Red) / (NIR + 6 × Red - 7.5 × Blue + 1))
- **Faixa de valores:** -1 a +2
- **Interpretação:**
  - > 0.5: Cobertura vegetal excelente
  - 0.3 - 0.5: Cobertura vegetal boa
  - < 0.3: Cobertura vegetal baixa
- **Vantagens:** Corrige saturação do NDVI e efeitos atmosféricos

### SAVI (Soil Adjusted Vegetation Index)
- **Referência Original:** Huete, A. R. (1988). A soil-adjusted vegetation index (SAVI). *Remote Sensing of Environment*, 25(3), 295-309. https://doi.org/10.1016/0034-4257(88)90106-X
- **Fórmula:** SAVI = ((NIR - Red) / (NIR + Red + L)) × (1 + L)
  - Onde L = 0.5 (fator de ajuste de solo)
- **Faixa de valores:** -1.5 a +1.5
- **Interpretação:** Similar ao NDVI, mas com correção para influência do solo

### ARVI (Atmospherically Resistant Vegetation Index)
- **Referência Original:** Kaufman, Y. J., & Tanré, D. (1992). Atmospherically resistant vegetation index (ARVI) for EOS-MODIS. *IEEE Transactions on Geoscience and Remote Sensing*, 30(2), 261-270. https://doi.org/10.1109/36.134076
- **Fórmula:** ARVI = (NIR - (2 × Red - Blue)) / (NIR + (2 × Red - Blue))
- **Faixa de valores:** 0.4 a +2
- **Interpretação:** Resistente a efeitos atmosféricos, especialmente aerossóis

---

## 🗄️ CONTROLE DE VERSÃO E HOSPEDAGEM

### Git
- **Descrição:** Sistema de controle de versão distribuído
- **Referência:** Chacon, S., & Straub, B. (2014). *Pro Git* (2nd ed.). Apress. https://git-scm.com/book/en/v2
- **Uso no projeto:** Versionamento de código e documentação

### GitHub
- **Descrição:** Plataforma de hospedagem de código
- **Referência:** GitHub, Inc. (2024). *GitHub Documentation*. https://docs.github.com/
- **Uso no projeto:** Repositório do projeto

### GitHub Pages
- **Descrição:** Hospedagem de sites estáticos
- **Referência:** GitHub, Inc. (2024). *GitHub Pages Documentation*. https://docs.github.com/en/pages
- **Uso no projeto:** Hospedagem dos mapas interativos online

---

## 🏛️ DADOS INSTITUCIONAIS

### Shapefiles dos Parques
- **Fonte:** Instituto Chico Mendes de Conservação da Biodiversidade (ICMBio)
- **Dados:**
  - Limite do Parque Nacional de São Joaquim (45.524 ha)
  - Limite do Parque Estadual da Serra Furada (1.330 ha, 6 zonas)
  - Cidades afetadas pelo PARNA

### Limites Territoriais
- **Fonte:** Instituto Brasileiro de Geografia e Estatística (IBGE)
- **Dados:**
  - Limites municipais de Santa Catarina (2024)
  - Limite estadual de Santa Catarina (2024)

### Coordenadas das Parcelas
- **Fonte:** Programa PELD-BISC
- **Dados:**
  - 49 parcelas de monitoramento (29 terrestres, 20 ripárias)
  - Distribuídas em 3 módulos (M1, M2, M3)

---

## 🏛️ INSTITUIÇÕES ENVOLVIDAS

### Universidade Federal de Santa Catarina (UFSC)
- Instituição responsável pelo projeto PELD-BISC
- https://ufsc.br/

### Programa de Pesquisa Ecológica de Longa Duração (PELD)
- Financiamento: CNPq (Conselho Nacional de Desenvolvimento Científico e Tecnológico)
- https://peld.cnpq.br/

### Instituto Chico Mendes de Conservação da Biodiversidade (ICMBio)
- Gestão das unidades de conservação
- https://www.gov.br/icmbio/

---

## 📄 LICENÇA E USO

Este projeto foi desenvolvido para fins **acadêmicos e de pesquisa** no âmbito do Programa PELD-BISC (Biodiversidade de Santa Catarina).

### Uso Permitido:
- ✅ Pesquisa científica e acadêmica
- ✅ Educação e ensino
- ✅ Divulgação científica
- ✅ Referência em trabalhos acadêmicos

### Citação Recomendada:
```
Caetano, R. A. (2025). Mapas Interativos do Programa PELD - Biodiversidade de Santa Catarina. 
Universidade Federal de Santa Catarina. 
Disponível em: https://caetanoronan.github.io/mapa-peld-santa-catarina/
```

---

## 🙏 AGRADECIMENTOS

- **Equipe PELD-BISC** pela disponibilização dos dados de monitoramento
- **ICMBio** pelos shapefiles das unidades de conservação
- **USGS** pela disponibilização gratuita de imagens Landsat
- **CNPq** pelo financiamento do programa PELD
- **Comunidade Open Source** pelos softwares e bibliotecas utilizadas
- **GitHub Copilot** pela assistência no desenvolvimento

---

## 📞 CONTATO

**Ronan Armando Caetano**
- Email: caetanoronan@gmail.com
- Instituição: Universidade Federal de Santa Catarina (UFSC)
- Programa: PELD-BISC - Biodiversidade de Santa Catarina

---

## 🔗 LINKS DO PROJETO

- **Repositório GitHub:** https://github.com/caetanoronan/mapa-peld-santa-catarina
- **Dashboard Online:** https://caetanoronan.github.io/mapa-peld-santa-catarina/dashboard_peld.html
- **Mapas Interativos:** https://caetanoronan.github.io/mapa-peld-santa-catarina/
 - **Mapas Interativos:** https://caetanoronan.github.io/mapa-peld-santa-catarina/ (ver destaque: `mapa_simples_completo.html`)
 - **Mapa Simples Completo (destaque):** https://caetanoronan.github.io/mapa-peld-santa-catarina/mapa_simples_completo.html

---

*Documento atualizado em: 01 de novembro de 2025*

*Desenvolvido com 💚 para conservação da biodiversidade de Santa Catarina*
