@echo off
setlocal EnableDelayedExpansion

:: Retrieve the screensaver timeout setting in seconds from the registry
for /f "tokens=2*" %%a in ('reg query "HKEY_CURRENT_USER\Control Panel\Desktop" /v ScreenSaveTimeOut') do set ScreenSaverTimeSec=%%b

:: Convert the timeout from seconds to minutes
set /a ScreenSaverTimeMin=!ScreenSaverTimeSec! / 60

:: Check if the screensaver timeout is 10 minutes or more
if !ScreenSaverTimeMin! geq 10 (
    echo 양호
    echo 현재 상태: 화면 보호기 !ScreenSaverTimeMin! 분 설정 중
    goto endScript
)

:: If the above condition is not met, this part will execute
echo 미흡
echo 현재 상태: 화면 보호기 설정 시간이 !ScreenSaverTimeMin! 분으로 변경 필요
echo 조치 방법: SKT AD를 통해 제어되는 부분으로 AD 재설치가 필요합니다.

:endScript
endlocal

