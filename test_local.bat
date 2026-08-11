@echo off
setlocal
cd /d "%~dp0"
title 200alaronde V3 - Test local
echo.
echo ==========================================
echo   200alaronde V3 - Test local
echo ==========================================
echo.
where python >nul 2>&1
if %errorlevel%==0 (
  python build.py
  start "" http://localhost:8000
  python -m http.server 8000
  goto :end
)
where py >nul 2>&1
if %errorlevel%==0 (
  py build.py
  start "" http://localhost:8000
  py -m http.server 8000
  goto :end
)
echo ERREUR : Python n'a pas ete trouve.
pause
:end
endlocal
