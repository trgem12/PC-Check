@echo off

:: 변수 초기화
set /a Sel5 = 1
set b=0
set SCRNSAVE_VALUE=""

:: ScreenSaveActive 존재 여부 확인
for /f "tokens=2* delims= " %%a in ('reg query "HKEY_CURRENT_USER\SOFTWARE\Policies\Microsoft\Windows\Control Panel\Desktop" ^| findstr /i "ScreenSaveActive"') do (
    if "%%b" == "1" (
        set /a Sel5 = 0
        set b=%%b
    )
)

REM HKEY_CURRENT_USER\SOFTWARE\Policies\Microsoft\Windows\Control Panel\Desktop

:: SCRNSAVE.EXE 존재 여부 확인
set SCRNSAVE_SET=0
for /f "tokens=2* delims= " %%a in ('reg query "HKEY_CURRENT_USER\Control Panel\Desktop" ^| findstr /i "SCRNSAVE.EXE"') do (
    if not "%%b"=="" (
        set SCRNSAVE_SET=1
        set SCRNSAVE_VALUE=%%b
    )
)

:: ScreenSaveActive 및 SCRNSAVE.EXE 존재 여부 확인 후 출력
if %Sel5% == 1 (
    echo 미흡
    echo 현재 상태: 화면 보호기 설정이 되어 있지 않습니다.
    echo 조치 방법:
    echo 1. 레지스트리 HKEY_CURRENT_USER\SOFTWARE\Policies\Microsoft\Windows\Control Panel\Desktop\ScreenSaveActive 값을 1로 변경해주세요.
    echo 2. 레지스트리 값이 없다면 Help Desk 문의 후 화면 보호기 재설정 바랍니다.
) else if %SCRNSAVE_SET% == 0 (
    echo 미흡
    echo 현재 상태: SCRNSAVE.EXE 값이 설정되어 있지 않습니다.
    echo 조치 방법: 화면보호기 변경 → OSN 화면보호기 클릭 → 확인
) else (
    echo 양호
    echo 현재 상태: ONS 화면 보호기가 설정되어 있습니다. ScreenSaveActive 값: %b%, SCRNSAVE.EXE 값: %SCRNSAVE_VALUE%
)