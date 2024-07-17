@echo off
setlocal EnableDelayedExpansion

:: ScreenSaveTimeOut 값이 있는지 확인
set ScreenSaveTimeOutExists=0
for /f "tokens=2*" %%a in ('reg query "HKEY_CURRENT_USER\SOFTWARE\Policies\Microsoft\Windows\Control Panel\Desktop" /v ScreenSaveTimeOut 2^>nul') do (
    set ScreenSaveTimeOutExists=1
    set ScreenSaverTimeSec=%%b
)

:: ScreenSaveTimeOut 값이 존재하는지 확인
if %ScreenSaveTimeOutExists% == 0 (
    echo 미흡
    echo 현재 상태: HKEY_CURRENT_USER\SOFTWARE\Policies\Microsoft\Windows\Control Panel\Desktop 레지스트리 경로에 ScreenSaveTimeOut 값이 존재하지 않습니다.
    echo 조치 방법: Help Desk 문의 또는 AD 재설치 바랍니다.
    goto endScript
)

:: ScreenSaverTimeSec 값이 600초 이상인지 확인
if !ScreenSaverTimeSec! geq 600 (
    echo 양호
    echo 현재 상태: 화면 보호기가 !ScreenSaverTimeSec! 초로 설정되어 있습니다.
) else (
    echo 미흡
    echo 현재 상태: 화면 보호기 설정 시간이 !ScreenSaverTimeSec! 초로 설정되어 있습니다. 600초로 변경이 필요합니다.
    echo 조치 방법: 
    echo 1. 레지스트리 \HKEY_CURRENT_USER\SOFTWARE\Policies\Microsoft\Windows\Control Panel\Desktop\ScreenSaveTimeOut 값을 600으로 변경 또는
    echo 2. CMD → gpupdate /force 입력.
)

:endScript
endlocal