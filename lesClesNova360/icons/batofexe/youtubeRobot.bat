::[Bat To Exe Converter]
::
::YAwzoRdxOk+EWAjk
::fBw5plQjdCuDJFeL4kNjfktoZQqRKGq2CrQI4ef1/NaLp14+WOcsVoDN2+fYcNwa6UrqZqok1XVUl80JFB5kZx2+eho2rCNOuWOKeteStEKyHxDZq3w5FWF7kHCehSg0AA==
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
::Zh4grVQjdCuDJFeL4kNjfktoZQqRKGq2CrQI4ef1/NaLp14+WOcsVoDN2+fYcNwa6UrqZqoozn95lM4wFQ9aMBeza28=
::YB416Ek+ZG8=
::
::
::978f952a14a936cc963da21a135fa983
@ECHO OFF
chcp 65001 > nul

:: Script to gather system information and execute YouTube automation robots in parallel

:: Set colors: white text on a dark red background, matching YouTube's brand color
COLOR 4F

:: Set CMD window title and minimal size
TITLE AI YOUTUBE ROBOT PRO - System Insights & YouTube Execution
MODE con: cols=60 lines=15

:: Clear screen
CLS

:: Display YouTube-inspired banner
ECHO ==============================================================================
ECHO                            AI YOUTUBE ROBOT PRO                             
ECHO ==============================================================================
ECHO                Preparing to launch your YouTube automation robots...             
ECHO ==============================================================================
ECHO.
ECHO Gathering system information... Please hold on...
ECHO.

:: Initialize robot counter
SET robot_count=0

:: Find hidden folders in C:\youtubebot that start with "robot"
FOR /F "tokens=*" %%D IN ('DIR /A:DH /B C:\ytbot\robot*') DO (
    SET /A robot_count+=1
)

:: Display the number of robot directories found
ECHO ==============================================================================
ECHO %robot_count% hidden YouTube robot directories detected.
ECHO ==============================================================================

:: Exit if no robot folders found
IF %robot_count%==0 (
    ECHO No YouTube robot directories found. Exiting the program.
    ECHO ==============================================================================
    PAUSE
    EXIT /B
)

:: Start each robot
ECHO.
ECHO ==============================================================================
ECHO Launching YouTube robots. Please wait...
ECHO ==============================================================================

:: Loop to launch each robot in a separate minimized CMD window
FOR /L %%i IN (1,1,%robot_count%) DO (
    ECHO ==============================================================================
    ECHO Launching Robot %%i in a new window...
    ECHO ==============================================================================

    :: Open new CMD with unique title, running minimized
    start /MIN "Robot %%i" cmd /c "
    TITLE YouTube Robot %%i - AI YOUTUBE ROBOT PRO
    COLOR 4F
    MODE con: cols=50 lines=10
    ECHO ==============================================================================
    ECHO Activating environment for YouTube Robot %%i...
    ECHO ==============================================================================
    cd /d C:\ytbot\robot%%i\env%%i\Scripts
    call activate
    
    ECHO ==============================================================================
    ECHO Navigating to the directory for Robot %%i...
    ECHO ==============================================================================
    cd /d C:\ytbot\robot%%i
    
    ECHO ==============================================================================
    ECHO Running YouTube Robot %%i script...
    ECHO ==============================================================================
    python __post_youtube__.py
    
    ECHO ==============================================================================
    ECHO YouTube Robot %%i process complete.
    ECHO ==============================================================================
    PAUSE
    "
)

ECHO ==============================================================================
ECHO All YouTube robots have been successfully launched in separate minimized windows.
ECHO ==============================================================================
PAUSE
