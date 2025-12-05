@echo off
setlocal enabledelayedexpansion

echo ========================================================
echo   MSR 2026 Artifact — One-Click Reproduction Script
echo ========================================================
echo.

REM ----------------------------------------
REM 1. Check if conda exists
REM ----------------------------------------
where conda >nul 2>&1
IF ERRORLEVEL 1 (
    echo [ERROR] Conda was not found on your system.
    echo Please install Miniconda or Anaconda before running this script.
    pause
    exit /b 1
)

echo [1/4] Checking Conda environment...

set ENV_NAME=msr2026

REM Check if environment exists
call conda info --envs | findstr /R /C:"%ENV_NAME%" >nul
IF ERRORLEVEL 1 (
    echo Environment %ENV_NAME% not found.
    echo Creating environment from environment.yml...
    call conda env create -f environment.yml
) ELSE (
    echo ✔ Environment "%ENV_NAME%" already exists.
)

echo Activating environment...
call conda activate %ENV_NAME%
echo ✔ Conda environment ready.
echo.

REM ----------------------------------------
REM 2. Set PYTHONPATH
REM ----------------------------------------
echo [2/4] Setting PYTHONPATH...

set SRC_PATH=%cd%\src
set PYTHONPATH=%SRC_PATH%
echo ✔ PYTHONPATH set to include src/
echo.

REM ----------------------------------------
REM 3. Run the main pipeline
REM ----------------------------------------
echo [3/4] Running full MSR pipeline...
python main_run_all.py

IF ERRORLEVEL 1 (
    echo [ERROR] Python execution failed.
    pause
    exit /b 1
)

echo ✔ All RQs executed successfully.
echo.

REM ----------------------------------------
REM 4. Completion message
REM ----------------------------------------
echo [4/4] All results generated!
echo Figures saved to:  output\figures\
echo Tables saved to:   output\tables\
echo.
echo ========================================================
echo           Artifact Reproduction Completed!
echo ========================================================
echo.

pause
