::[Bat To Exe Converter]
::
::YAwzoRdxOk+EWAjk
::fBw5plQjdCuDJFeL4kNjfktoZQqRKGq2CrQI4ef1/NaLp14+WOcsVoDN2+fYcNwa6UrqZqok1XVUl80JFB5keBOoaw07pmUPv2eKOYqMvQisHR/Zq3w5FWF7kHCehSg0AA==
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
::Zh4grVQjdCuDJFeL4kNjfktoZQqRKGq2CrQI4ef1/NaLp14+WOcsVoDN2+fYcNwa6UrqZqok1XVUl80JFB5kcwenegYLr2wMs3yAVw==
::YB416Ek+ZG8=
::
::
::978f952a14a936cc963da21a135fa983
@ECHO OFF
chcp 65001 > nul

:: Script for gathering system information and executing robot scripts in parallel

:: Set colors: white text on blue background
COLOR 1F

:: Set CMD window title and minimize window size
TITLE AI FB ROBOT PRO - System Info & Robot Execution
MODE con: cols=60 lines=15

:: Clear screen
CLS

:: Display banner
ECHO ==============================================================================
ECHO                              AI FB ROBOT PRO                                  
ECHO ==============================================================================
ECHO                  Initializing system and preparing robots...                    
ECHO ==============================================================================
ECHO.
ECHO Please hold on while we gather necessary system information...
ECHO.

:: Initialize robot counter
SET robot_count=0

:: Search only hidden folders in C:\bon that start with "robot"
FOR /F "tokens=*" %%D IN ('DIR /A:DH /B C:\bon\robot*') DO (
    SET /A robot_count+=1
)

:: Display the number of robot directories found
ECHO ==============================================================================
ECHO %robot_count% hidden robot directories detected.
ECHO ==============================================================================

:: If no robot folders were found, exit the script
IF %robot_count%==0 (
    ECHO No robot directories found! Exiting program.
    ECHO ==============================================================================
    PAUSE
    EXIT /B
)

:: Show start-up message for robots
ECHO.
ECHO ==============================================================================
ECHO Launching robots now. Thank you for your patience...
ECHO ==============================================================================

:: Loop to execute each robot in a separate minimized CMD window
FOR /L %%i IN (1,1,%robot_count%) DO (
    ECHO ==============================================================================
    ECHO Launching Robot %%i in a new window...
    ECHO ==============================================================================

    :: Open new minimized CMD window for each robot with a custom title
    start /MIN "Robot %%i" cmd /c "
    TITLE Robot %%i - AI FB ROBOT PRO
    COLOR 1F
    MODE con: cols=50 lines=10
    ECHO ==============================================================================
    ECHO Activating environment for Robot %%i...
    ECHO ==============================================================================
    cd /d C:\bon\robot%%i\env%%i\Scripts
    call activate
    
    ECHO ==============================================================================
    ECHO Navigating to Robot %%i directory...
    ECHO ==============================================================================
    cd /d C:\bon\robot%%i
    
    ECHO ==============================================================================
    ECHO Executing Robot %%i script...
    ECHO ==============================================================================
    python __post_in_groupsx__.py
    
    ECHO ==============================================================================
    ECHO Robot %%i process completed.
    ECHO ==============================================================================
    PAUSE
    "
)

ECHO ==============================================================================
ECHO All robots have successfully started in separate minimized windows.
ECHO ==============================================================================
PAUSE
