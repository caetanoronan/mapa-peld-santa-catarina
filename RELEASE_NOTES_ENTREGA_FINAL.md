# Release: Entrega Final PELD - Pacote de Entrega (ZIP)

Data: 2025-11-19
Tag recomendada: `v1.0-entrega`

## Conteúdo do Pacote
- `dashboard_entrega_relatorio_final.html` — Página de entrega com links e explicações dos produtos.
- `mapa_simples_completo.html` — Mapa principal com todas as parcelas.
- `dashboard_ppBio_interativo.html` — Dashboard interativo com gráficos e mapa.
- `comparacao_mapas_visual.html` — Comparação visual do planejado vs implementado.
- `RELATORIO_ENTREGA.pdf` — Relatório consolidado (sumário).
- `RELATORIO_ENTREGA_COM_FIGURAS.pdf` — Relatório com figuras e gráficos.
- `RELATORIO_ENTREGA_FINAL_COM_MAPAS.pdf` — Relatório com screenshots dos mapas.
- `RELATORIO_ENTREGA_LIGHT.pdf` — Versão leve do relatório (otimizada para GitHub Pages).
- `amb_csv/` — CSV principal com coordenadas (copiado para o pacote).

## Notas do Release
- Este release consolida o pacote utilizado para a defesa/entrega final do PELD-Santa Catarina.
- O ZIP contém tanto os recursos interativos (HTML) quanto relatórios em PDF e os dados (CSV) necessários para reprodução local.
- O arquivo `RELATORIO_ENTREGA_LIGHT.pdf` foi adicionado para garantir compatibilidade com GitHub Pages (download mais rápido e menor probabilidade de 404/CDN issues).

## Como usar
1. Baixe o ZIP (arquivo anexado no Release). 
2. Extraia o conteúdo em uma pasta local. 
3. Abra `dashboard_entrega_relatorio_final.html` em um navegador para acessar os links e baixar os PDFs.

## Observações técnicas
- Algumas imagens e PDFs grandes estão gerenciadas com Git LFS no repositório principal; caso necessite baixar tudo manualmente, use a Release para obter o ZIP com todos os artefatos.
- Se preferir versão online, os links diretos estão hospedados em GitHub Pages (veja `dashboard_peld.html` para acesso rápido).

## Créditos
- Autor: Ronan Armando Caetano
- Assistência de desenvolvimento: GitHub Copilot (IA de assistência)

---

Se quiser, eu crio o texto de descrição do Release com um resumo curto e as instruções que você pode colar diretamente no campo "Release notes" ao criar o Release via web UI ou CLI.
