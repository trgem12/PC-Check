@echo off

:: Initialize the variable to indicate screensaver not set
set /a Sel5 = 1

:: Check the registry for SCRNSAVE.EXE setting
for /f "tokens=2* delims= " %%a in ('reg query "HKEY_CURRENT_USER\Control Panel\Desktop" ^| findstr /i "SCRNSAVE.EXE"') do (
    if not "%%b" == "" (
        set /a Sel5 = 0
        echo 양호
        echo 현재 상태: %%b 화면 보호기가 설정되어 있습니다.
    )
)

:: Check if screensaver is not set and display message
if %Sel5% == 1 (
    echo 미흡
    echo 현재 상태: 화면 보호기 설정이 되어 있지 않습니다.
    echo 조치 방법: SKT AD를 통해 제어되는 부분으로 AD 재설치가 필요합니다.
)

pause