@echo off
:menu
cls
echo ==========================================
echo       PYTHON SCRIPT SELECTOR
echo ==========================================
echo  [0] Run Equation Solver
echo  [1] Run Graphs
echo  [2] Run Integration
echo  [3] Run Differentiation
echo  [q] Quit
echo ==========================================
set /p userinput="Enter your choice (0-3): "

if "%userinput%"=="0" pythonw e.pyw
if "%userinput%"=="1" pythonw g.pyw
if "%userinput%"=="2" pythonw i.pyw
if "%userinput%"=="3" pythonw d.pyw
if "%userinput%"=="q" exit

echo.
echo Task finished. Press any key to return to menu...
pause >nul
goto menu