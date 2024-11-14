@echo off
set SCRIPT_NAME=pipeline_chi2.py 

REM Boucles pour chaque combinaison d'arguments
for %%a in (features graphfeatures) do (
    for %%b in (leaks outages hijack) do (
        echo Execution avec les arguments %%a et %%b...
        python %SCRIPT_NAME% %%a %%b
        if exist model_performance_chi2.csv (
            move model_performance_chi2.csv modele_performance_chi2_%%a_%%b.csv
        )
    )
)

echo Termine !
pause