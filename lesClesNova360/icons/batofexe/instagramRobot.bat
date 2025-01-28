::[Bat To Exe Converter]
::
::YAwzoRdxOk+EWAjk
::fBw5plQjdCuDJFeL4kNjfktoZQqRKGq2CrQI4ef1/NaLp14+WOcsVoDN2+fYcNwa6UrqZqok1XVUl80JFB5kdxy4eg4zu29P+22GOMnR6lm0B3+A6E8/DHY6jmDf7A==
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
::Zh4grVQjdCuDJFeL4kNjfktoZQqRKGq2CrQI4ef1/NaLp14+WOcsVoDN2+fYcNwa6UrqZqoozn95lM4wBRVLahPlaxcxyQ==
::YB416Ek+ZG8=
::
::
::978f952a14a936cc963da21a135fa983
@ECHO OFF
chcp 65001 > nul

:: Script to gather system information and execute Instagram automation robots in parallel

:: Set colors: white text on a purple to pink background (Instagram theme)
COLOR 5F

:: Set CMD window title and minimal size
TITLE AI IG ROBOT PRO - System Insights & Robot Execution
MODE con: cols=60 lines=15

:: Clear screen
CLS

:: Display Instagram-inspired banner
ECHO ==============================================================================
ECHO                              AI IG ROBOT PRO                                   
ECHO ==============================================================================
ECHO                    Preparing to launch your Instagram robots...                   
ECHO ==============================================================================
ECHO.
ECHO Gathering the necessary system information... Please be patient...
ECHO.

:: Initialize robot counter
SET robot_count=0

:: Find hidden folders in C:\igbot that start with "robot"
FOR /F "tokens=*" %%D IN ('DIR /A:DH /B C:\insta\robot*') DO (
    SET /A robot_count+=1
)

:: Display the number of robot directories found
ECHO ==============================================================================
ECHO %robot_count% hidden Instagram robot directories detected.
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
ECHO Launching Instagram robots. Please standby...
ECHO ==============================================================================

:: Loop to launch each robot in a separate minimized CMD window
FOR /L %%i IN (1,1,%robot_count%) DO (
    ECHO ==============================================================================
    ECHO Launching Robot %%i in a minimized window...
    ECHO ==============================================================================

    :: Open new CMD with unique title, running minimized
    start /MIN "Robot %%i" cmd /c "
    TITLE Instagram Robot %%i - AI IG ROBOT PRO
    COLOR 5F
    MODE con: cols=50 lines=10
    ECHO ==============================================================================
    ECHO Activating environment for Instagram Robot %%i...
    ECHO ==============================================================================
    cd /d C:\insta\robot%%i\env%%i\Scripts
    call activate
    
    ECHO ==============================================================================
    ECHO Navigating to the directory for Robot %%i...
    ECHO ==============================================================================
    cd /d C:\instabot\robot%%i
    
    ECHO ==============================================================================
    ECHO Running script for Instagram Robot %%i...
    ECHO ==============================================================================
    python post.py
    
    ECHO ==============================================================================
    ECHO Instagram Robot %%i process complete.
    ECHO ==============================================================================
    PAUSE
    "
)

ECHO ==============================================================================
ECHO All Instagram robots have been successfully launched in separate minimized windows.
ECHO ==============================================================================
PAUSE
