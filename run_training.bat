@echo off
title Train Rainfall Prediction ML Models - Aditya Saini
echo ========================================================
echo   Training Machine Learning Models (Aditya Saini)
echo ========================================================
echo.
python src\train_model.py
echo.
echo Generating Academic Project Report (.docx)...
python reports\generate_report_docx.py
echo.
echo Done! All models, graphs, and docx report have been updated.
pause
