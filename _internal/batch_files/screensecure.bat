@echo off

:: Initialize the variable to indicate screensaver not set
set /a Sel5 = 1
set b=0

:: Check the registry for ScreenSaverIsSecure setting
for /f "tokens=2* delims= " %%a in ('reg query "HKEY_CURRENT_USER\SOFTWARE\Policies\Microsoft\Windows\Control Panel\Desktop" ^| findstr /i "ScreenSaverIsSecure"') do (
    set b=%%b
    if "%%b" == "1" (
        set /a Sel5 = 0
        echo 양호
        echo 현재 상태: 화면 보호기가 암호화되어 있습니다. ScreenSaverIsSecure 값: %%b
    )
)

:: Check if screensaver is not set and display message
if %Sel5% == 1 (
    echo 미흡
    echo 현재 상태: 화면 보호기가 암호화되어 있지 않습니다. ScreenSaverIsSecure 값: %b%
    echo 조치 방법: Help Desk에 화면보호기 오류 문의 바랍니다.
)