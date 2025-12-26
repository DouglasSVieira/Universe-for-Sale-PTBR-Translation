@echo off
title Atualizador de Traducao - Universe for Sale
echo 🚀 Iniciando exportacao de Dialogos...
python exportar_limpo.py
echo.
echo 📦 Iniciando exportacao de Dados (Sistema/Objetos)...
python exportar_data.py
echo.
echo ✅ PROCESSO CONCLUIDO! Pressione qualquer tecla para fechar.
pause