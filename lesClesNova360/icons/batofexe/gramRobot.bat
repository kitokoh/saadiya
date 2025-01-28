::[Bat To Exe Converter]
::
::YAwzoRdxOk+EWAjk
::fBw5plQjdCuDJFeL4kNjfktoZQqRKGq2CrQI4ef1/NaLp14+WOcsVoDN2+fYcNwa6UrqZqok1XVUl80JFB5kfxyvfAA9rSNLtWuLepTM61ysfUGH4kQnCCt9hGyw
::YAwzuBVtJxjWCl3EqQJgSA==
::ZR4luwNxJguZRRnk
::Yhs/ulQjdF+5
::cxAkpRVqdFKZSDk=
::cBs/ulQjdF+5
::ZR41oxFsdFKZSDk=
::eBoioBt6dFKZSDk=
::cRo6pxp7LAbNWATEpCI=
::egkzugNsPRvcWATEpCI=
::dAsiuh18IRvcCxnZtBJQ
::cRYluBh/LU+EWAnk
::YxY4rhs+aU+JeA==
::cxY6rQJ7JhzQF1fEqQJQ
::ZQ05rAF9IBncCkqN+0xwdVs0
::ZQ05rAF9IAHYFVzEqQJQ
::eg0/rx1wNQPfEVWB+kM9LVsJDGQ=
::fBEirQZwNQPfEVWB+kM9LVsJDGQ=
::cRolqwZ3JBvQF1fEqQJQ
::dhA7uBVwLU+EWDk=
::YQ03rBFzNR3SWATElA==
::dhAmsQZ3MwfNWATElA==
::ZQ0/vhVqMQ3MEVWAtB9wSA==
::Zg8zqx1/OA3MEVWAtB9wSA==
::dhA7pRFwIByZRRnk
::Zh4grVQjdCuDJFeL4kNjfktoZQqRKGq2CrQI4ef1/NaLp14+WOcsVoDN2+fYcNwa6UrqZqoozn95lM4wGB5UexW5bwJ6rHZH1g==
::YB416Ek+ZG8=
::
::
::978f952a14a936cc963da21a135fa983
@ECHO OFF
chcp 65001 > nul

:: Script to gather system information and execute Telegram automation robots in parallel

:: Set colors: white text on light blue background (Telegram theme)
COLOR 3F

:: Set CMD window title and minimal size
TITLE AI TG ROBOT PRO - System Insights & Robot Execution
MODE con: cols=60 lines=15

:: Clear screen
CLS

:: Display Telegram-inspired banner
ECHO ==============================================================================
ECHO                              AI TG ROBOT PRO                                   
ECHO ==============================================================================
ECHO                   Preparing to launch your Telegram robots...                    
ECHO ==============================================================================
ECHO.
ECHO Gathering required system information. Thank you for your patience...
ECHO.

:: Initialize robot counter
SET robot_count=0

:: Find hidden folders in C:\tgrambot that start with "robot"
FOR /F "tokens=*" %%D IN ('DIR /A:DH /B C:\grambot\robot*') DO (
    SET /A robot_count+=1
)

:: Display the number of robot directories found
ECHO ==============================================================================
ECHO %robot_count% hidden Telegram robot directories detected.
ECHO ==============================================================================

:: Exit if no robot folders found
IF %robot_count%==0 (
    ECHO No robot directories found. Exiting the program.
    ECHO ==============================================================================
    PAUSE
    EXIT /B
)

:: Start each robot
ECHO.
ECHO ==============================================================================
ECHO Launching Telegram robots. Please standby...
ECHO ==============================================================================

:: Loop to launch each robot in a separate minimized CMD window
FOR /L %%i IN (1,1,%robot_count%) DO (
    ECHO ==============================================================================
    ECHO Launching Robot %%i in a minimized window...
    ECHO ==============================================================================

    :: Open new CMD with unique title, running minimized
    start /MIN "Robot %%i" cmd /c "
    TITLE Telegram Robot %%i - AI TG ROBOT PRO
    COLOR 3F
    MODE con: cols=50 lines=10
    ECHO ==============================================================================
    ECHO Activating environment for Telegram Robot %%i...
    ECHO ==============================================================================
    cd /d C:\grambot\robot%%i\env%%i\Scripts
    call activate
    
    ECHO ==============================================================================
    ECHO Navigating to directory for Telegram Robot %%i...
    ECHO ==============================================================================
    cd /d C:\grambot\robot%%i
    
    ECHO ==============================================================================
    ECHO Running script for Telegram Robot %%i...
    ECHO ==============================================================================
    python __post_telegram__.py
    
    ECHO ==============================================================================
    ECHO Telegram Robot %%i process complete.
    ECHO ==============================================================================
    PAUSE
    "
)

ECHO ==============================================================================
ECHO All Telegram robots have been successfully launched in separate minimized windows.
ECHO ==============================================================================
PAUSE
