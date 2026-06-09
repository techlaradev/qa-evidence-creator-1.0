@echo off
cd /d %~dp0
echo Bem vinde ao QA Evidence Maker...
py -m pip install -r requirements.txt

echo Iniciando app...
echo APP FEITO POR LARA CARDOSO 
py -m streamlit run generate.py

echo APP FEITO POR LARA CARDOSO 
pause