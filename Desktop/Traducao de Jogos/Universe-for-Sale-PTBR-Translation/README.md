# 🪐 Tradução PT-BR: Universe for Sale

**Status:** EM ANDAMENTO (Revisão Final) | **Última Atualização:** 23/12/2025

## 📝 Sobre o Projeto

Este projeto é uma iniciativa de fã para traduzir o jogo de aventura narrativa **Universe for Sale**, desenvolvido pela Tmesis Studio, para o Português Brasileiro (PT-BR). O objetivo é tornar a experiência completa da história acessível à comunidade brasileira.

## 🛠️ Progresso

| Etapa | Status | Detalhes |
| :--- | :--- | :--- |
| Extração de Texto | ✅ COMPLETA | Arquivos .json localizados e convertidos para planilha. |
| **Tradução** | ✅ COMPLETA | Tradução de 100% das 4.429 strings de texto (Base Espanhola). | 
| Revisão (QC) | ⏳ EM TESTE | Revisão fina para otimizar o espaço em tela e a fluidez das gírias. |  
| Teste Técnico | ✅ COMPLETO | Estabilidade confirmada com novos scripts de exportação. |
| Criação do Patch | ❌ PENDENTE | Será iniciada após a conclusão dos testes (QC). | 

## ⚙️ Ajustes Técnicos Realizados

* **Compatibilidade de Fonte:** O texto foi convertido para **MAIÚSCULAS** e os acentos foram removidos (ex: "MAMÃE" → "MAMAE") via script automatizado (`exportar_limpo.py`). Isso evita erros visuais na fonte nativa do Construct 3.
* **Nova Base de Tradução (Espanhol):** A base de referência foi alterada do Inglês para o Espanhol. Esta escolha permite uma adaptação mais fluida e um melhor ajuste do texto nos balões de diálogo, evitando cortes (overflow).
* **Automação:** Foram desenvolvidos scripts em Python para garantir que a atualização da planilha reflita instantaneamente nos arquivos do jogo sem perda de dados.

## 📦 Arquivos de Tradução

Os arquivos finais traduzidos estão localizados na pasta `Translation/`:
* `dlg_choose_es.json`: Opções de escolha e ramificações da história.
* `dlg_dialoghi_es.json`: Corpo principal dos diálogos do jogo.
* `TRABALHO_BASE_ESPANHOL.csv`: Planilha mestre de controle da tradução.

## 👥 Créditos

### 🇧🇷 Projeto de Tradução e Modding
* **Liderança e Tradução:** DouglasSVieira
* **Ferramentas:** Python 3, Git/GitHub, Google Sheets

## ⚠️ Aviso Legal

Este é um projeto de fã, sem fins lucrativos. O repositório **não contém arquivos proprietários do jogo** (como binários ou pacotes .pak), apenas scripts de ferramentas e os arquivos de texto traduzidos para fins de estudo e colaboração.
