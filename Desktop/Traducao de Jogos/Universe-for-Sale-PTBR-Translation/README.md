# 🪐 Tradução PT-BR: Universe for Sale

**Status:** EM ANDAMENTO (Revisão Final) | **Última Atualização:** 26/12/2025

## 📝 Sobre o Projeto

Este projeto é uma iniciativa de fã para traduzir o jogo de aventura narrativa **Universe for Sale**, desenvolvido pela Tmesis Studio, para o Português Brasileiro (PT-BR). O objetivo é tornar a experiência completa da história acessível à comunidade brasileira.

## 🛠️ Progresso

| Etapa | Status | Detalhes |
| :--- | :--- | :--- |
| Extração de Texto | ✅ COMPLETA | Diálogos e arquivos de sistema (data.json/data_fix.json e dlg_choose_es.json/dlg_dialoghi_es.json) extraídos. |
| **Tradução** | ⏳ EM ANDAMENTO | Diálogos 100% / Interações de cenário em tradução.. | 
| Revisão (QC) | ⏳ EM TESTE | Revisão fina para otimizar o espaço em tela e a fluidez das gírias. |  
| Teste Técnico | ✅ COMPLETO | Sistema de duas planilhas operando sem conflitos. |
| Criação do Patch | ❌ PENDENTE | Será iniciada após a conclusão dos testes (QC). | 

## ⚙️ Ajustes Técnicos Realizados / Fluxo de Trabalho (Dual-Planilha)

* **Compatibilidade de Fonte:** O texto foi convertido para **MAIÚSCULAS** e os acentos foram removidos (ex: "MAMÃE" → "MAMAE") via script automatizado (`exportar_limpo.py`). Isso evita erros visuais na fonte nativa do Construct 3.
* **Nova Base de Tradução (Espanhol):** A base de referência foi alterada do Inglês para o Espanhol. Esta escolha permite uma adaptação mais fluida e um melhor ajuste do texto nos balões de diálogo, evitando cortes (overflow).
* **Automação:** Foram desenvolvidos scripts em Python para garantir que a atualização da planilha reflita instantaneamente nos arquivos do jogo sem perda de dados.

* **Para garantir a integridade dos dados, separamos o projeto em duas frentes:**

* **Diálogos (TRABALHO_BASE_ESPANHOL.csv):** Contém as falas principais dos personagens (Lila, Kaan, etc.).

* **Interações e Sistema (TRABALHO_DATA.csv):** Contém pensamentos do protagonista, descrições de objetos (como o bar) e termos técnicos.

* **Automação de Exportação**
* **Desenvolvemos scripts específicos para processar cada tipo de arquivo:**

* `exportar_limpo.py`: Processa os diálogos principais.

* `exportar_data.py`: Processa as interações e sistema (arquivos data.json).

* `ATUALIZAR_GAME.bat`: Um facilitador que executa ambos os scripts de uma só vez, aplicando todas as traduções ao jogo instantaneamente.

## 📦 Arquivos de Tradução

Os arquivos finais traduzidos estão localizados na pasta `Translation/`:
* `dlg_choose_es.json`: Opções de escolha e ramificações da história.
* `dlg_dialoghi_es.json`: Corpo principal dos diálogos do jogo.
* `data.json` / `data_fix.json`: Interações de cenário e scripts de sistema.
* `TRABALHO_BASE_ESPANHOL.csv`: Planilha mestre de controle da tradução.
* `TRABALHO_DATA.csv`: Planilha de controle de tradução de expressões.


## 👥 Créditos

### 🇧🇷 Projeto de Tradução e Modding
* **Liderança e Tradução:** DouglasSVieira
* **Ferramentas:** Python 3, Git/GitHub, Google Sheets

## ⚠️ Aviso Legal

Este é um projeto de fã, sem fins lucrativos. O repositório **não contém arquivos proprietários do jogo** (como binários ou pacotes .pak), apenas scripts de ferramentas e os arquivos de texto traduzidos para fins de estudo e colaboração.
