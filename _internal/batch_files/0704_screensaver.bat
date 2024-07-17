@echo off

:: Initialize the variable to indicate screensaver not set
set /a Sel5 = 1
set b=0

:: Check the registry for ScreenSaveActive setting
for /f "tokens=2* delims= " %%a in ('reg query "HKEY_CURRENT_USER\SOFTWARE\Policies\Microsoft\Windows\Control Panel\Desktop" ^| findstr /i "ScreenSaveActive"') do (
    if "%%b" == "1" (
        set /a Sel5 = 0
        set b=%%b
    )
)

:: Check the registry for SCRNSAVE.EXE setting
set SCRNSAVE_SET=0
for /f "tokens=2* delims= " %%a in ('reg query "HKEY_CURRENT_USER\Control Panel\Desktop" ^| findstr /i "SCRNSAVE.EXE"') do (
    if not "%%b"=="" (
        set SCRNSAVE_SET=1
    )
)

:: Check if screensaver is not set or SCRNSAVE.EXE is not set and display message
if %Sel5% == 1 (
    echo 미흡
    echo 현재 상태: 화면 보호기 설정이 되어 있지 않습니다.
    echo 조치 방법: Help Desk에 화면보호기 설정 오류 문의 바랍니다.
) else if %SCRNSAVE_SET% == 0 (
    echo 미흡
    echo 현재 상태: SCRNSAVE.EXE 값이 설정되어 있지 않습니다.
    echo 조치 방법: 화면보호기 설정 → 화면보호기 선택 후 확인 클릭
) else (
    echo 양호
    echo 현재 상태: 화면 보호기가 설정되어 있습니다. ScreenSaveActive 값: %b%
)