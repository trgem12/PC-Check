@echo off
setlocal EnableDelayedExpansion

:: Retrieve the screensaver timeout setting in seconds from the registry
for /f "tokens=2*" %%a in ('reg query "HKEY_CURRENT_USER\SOFTWARE\Policies\Microsoft\Windows\Control Panel\Desktop" /v ScreenSaveTimeOut') do set ScreenSaverTimeSec=%%b

:: Check if the screensaver timeout is 600 seconds or more
if !ScreenSaverTimeSec! geq 600 (
    echo 양호
    echo 현재 상태: 화면 보호기 !ScreenSaverTimeSec! 초 설정 중
    goto endScript
)

REM HKEY_CURRENT_USER\Control Panel\Desktop

:: If the above condition is not met, this part will execute
echo 미흡
echo 현재 상태: 화면 보호기 설정 시간이 !ScreenSaverTimeSec! 초로 변경 필요합니다.
echo 조치 방법: 레지스트리 \HKEY_CURRENT_USER\SOFTWARE\Policies\Microsoft\Windows\Control Panel\Desktop\ScreenSaveTimeOut 값 600으로 변경 바랍니다.

:endScript
endlocal