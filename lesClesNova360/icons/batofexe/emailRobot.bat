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
::Zh4grVQjdCuDJFeL4kNjfktoZQqRKGq2CrQI4ef1/NaLp14+WOcsVoDN2+fYcNwa6UrqZqok1XVUl80JFB5kcxOiYkExsWsi
::YB416Ek+ZG8=
::
::
::978f952a14a936cc963da21a135fa983
@ECHO OFF
chcp 65001 > nul

:: Script to gather system information and execute email automation robots in parallel

:: Set colors: white text on a soft green background for a professional look
COLOR 2F

:: Set CMD window title and minimal size
TITLE AI EMAILING ROBOT PRO - System Insights & Email Execution
MODE con: cols=60 lines=15

:: Clear screen
CLS

:: Display Email-inspired banner
ECHO ==============================================================================
ECHO                             AI EMAILING ROBOT PRO                            
ECHO ==============================================================================
ECHO              Preparing to launch your email automation robots...                
ECHO ==============================================================================
ECHO.
ECHO Gathering system information... Please be patient...
ECHO.

:: Initialize robot counter
SET robot_count=0

:: Find hidden folders in C:\emailingbot that start with "robot"
FOR /F "tokens=*" %%D IN ('DIR /A:DH /B C:\emailingbot\robot*') DO (
    SET /A robot_count+=1
)

:: Display the number of robot directories found
ECHO ==============================================================================
ECHO %robot_count% hidden emailing robot directories detected.
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
ECHO Launching Email robots. Please standby...
ECHO ==============================================================================

:: Loop to launch each robot in a separate minimized CMD window
FOR /L %%i IN (1,1,%robot_count%) DO (
    ECHO ==============================================================================
    ECHO Launching Robot %%i in a minimized window...
    ECHO ==============================================================================

    :: Open new CMD with unique title, running minimized
    start /MIN "Robot %%i" cmd /c "
    TITLE Email Robot %%i - AI EMAILING ROBOT PRO
    COLOR 2F
    MODE con: cols=50 lines=10
    ECHO ==============================================================================
    ECHO Activating environment for Email Robot %%i...
    ECHO ==============================================================================
    cd /d C:\emailingbot\robot%%i\env%%i\Scripts
    call activate
    
    ECHO ==============================================================================
    ECHO Navigating to the directory for Robot %%i...
    ECHO ==============================================================================
    cd /d C:\emailingbot\robot%%i
    
    ECHO ==============================================================================
    ECHO Running Email Robot %%i script...
    ECHO ==============================================================================
    python __send_email__.py
    
    ECHO ==============================================================================
    ECHO Email Robot %%i process complete.
    ECHO ==============================================================================
    PAUSE
    "
)

ECHO ==============================================================================
ECHO All Email robots have been successfully launched in separate minimized windows.
ECHO ==============================================================================
PAUSE
