<p align="center">
  <img src="assets/capa_dissertacao_entropia.gif" alt="Capa animada da dissertação Metodologia para o Ensino de Entropia Física via Noções de Teoria da Informação" width="100%">
</p>

# Produto educacional — Entropia Física e Teoria da Informação

Este repositório reúne os códigos, simulações e materiais computacionais desenvolvidos como parte da dissertação de mestrado intitulada **“Metodologia para o Ensino de Entropia Física via Noções de Teoria da Informação”**, de **Marcos Cavalcante Furtado**, vinculada ao **Mestrado Nacional Profissional em Ensino de Física — MNPEF, Polo 67/UNIFAP**.

A proposta integra entropia termodinâmica, entropia estatística e entropia informacional, com apoio de simulações em Python, incluindo o modelo de Ehrenfest, para favorecer a compreensão de microestados, macroestados, probabilidade, incerteza e equilíbrio estatístico.

## Pré-requisitos

Para utilizar os materiais deste produto educacional, recomenda-se:

- acesso a uma conta Google;
- uso do Google Colab para executar os notebooks;
- conhecimentos básicos de Física, probabilidade e interpretação de gráficos.

## Como utilizar o ambiente digital

Acesse o conteúdo desejado no repositório e abra o arquivo correspondente no Google Colab. O vídeo abaixo apresenta uma orientação inicial de uso:

https://github.com/user-attachments/assets/fbfbd6c6-62aa-4db9-8ed4-c82a6d1f4a6c

## Gerando novamente a capa do README

A capa animada é produzida inteiramente em Python com a biblioteca Pillow.

```bash
pip install pillow
python tools/gerar_capa_readme.py
```

O arquivo será salvo em:

```text
assets/capa_dissertacao_entropia.gif
```
