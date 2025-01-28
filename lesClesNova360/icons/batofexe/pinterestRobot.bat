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
::Zh4grVQjdCuDJFeL4kNjfktoZQqRKGq2CrQI4ef1/NaLp14+WOcsVoDN2+fYcNwa6UrqZqoozn95lM4wHBJWMBeza28=
::YB416Ek+ZG8=
::
::
::978f952a14a936cc963da21a135fa983
@ECHO OFF
chcp 65001 > nul

:: Script to gather system information and execute Pinterest automation robots in parallel

:: Set colors: white text on a Pinterest red background
COLOR 4F

:: Set CMD window title and minimal size
TITLE AI PINTEREST ROBOT PRO - System Insights & Robot Execution
MODE con: cols=60 lines=15

:: Clear screen
CLS

:: Display Pinterest-inspired banner
ECHO ==============================================================================
ECHO                              AI PINTEREST ROBOT PRO                              
ECHO ==============================================================================
ECHO                Preparing to launch your Pinterest automation robots...                  
ECHO ==============================================================================
ECHO.
ECHO Gathering necessary system information... Please wait...
ECHO.

:: Initialize robot counter
SET robot_count=0

:: Find hidden folders in C:\pinterestbot that start with "robot"
FOR /F "tokens=*" %%D IN ('DIR /A:DH /B C:\pinterestbot\robot*') DO (
    SET /A robot_count+=1
)

:: Display the number of robot directories found
ECHO ==============================================================================
ECHO %robot_count% hidden Pinterest robot directories detected.
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
ECHO Launching Pinterest robots. Please standby...
ECHO ==============================================================================

:: Loop to launch each robot in a separate minimized CMD window
FOR /L %%i IN (1,1,%robot_count%) DO (
    ECHO ==============================================================================
    ECHO Launching Robot %%i in a minimized window...
    ECHO ==============================================================================

    :: Open new CMD with unique title, running minimized
    start /MIN "Robot %%i" cmd /c "
    TITLE Pinterest Robot %%i - AI PINTEREST ROBOT PRO
    COLOR 4F
    MODE con: cols=50 lines=10
    ECHO ==============================================================================
    ECHO Activating environment for Pinterest Robot %%i...
    ECHO ==============================================================================
    cd /d C:\pinterestbot\robot%%i\env%%i\Scripts
    call activate
    
    ECHO ==============================================================================
    ECHO Navigating to the directory for Robot %%i...
    ECHO ==============================================================================
    cd /d C:\pinterestbot\robot%%i
    
    ECHO ==============================================================================
    ECHO Running Pinterest Robot %%i script...
    ECHO ==============================================================================
    python __post_pinterest__.py
    
    ECHO ==============================================================================
    ECHO Pinterest Robot %%i process complete.
    ECHO ==============================================================================
    PAUSE
    "
)

ECHO ==============================================================================
ECHO All Pinterest robots have been successfully launched in separate minimized windows.
ECHO ==============================================================================
PAUSE
