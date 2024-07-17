@echo off

:: 변수 초기화
set /a Sel5 = 1
set b=0
set SCRNSAVE_VALUE=""
set SCRNSAVE_ACTIVE_EXISTS=0
set SCRNSAVE_EXE_EXISTS=0

:: ScreenSaveActive 존재 여부 확인
for /f "tokens=2* delims= " %%a in ('reg query "HKEY_CURRENT_USER\SOFTWARE\Policies\Microsoft\Windows\Control Panel\Desktop" ^| findstr /i "ScreenSaveActive"') do (
    set SCRNSAVE_ACTIVE_EXISTS=1
    if "%%b" == "1" (
        set /a Sel5 = 0
        set b=%%b
    )
)

REM HKEY_CURRENT_USER\SOFTWARE\Policies\Microsoft\Windows\Control Panel\Desktop

:: SCRNSAVE.EXE 존재 여부 확인
for /f "tokens=2* delims= " %%a in ('reg query "HKEY_CURRENT_USER\Control Panel\Desktop" ^| findstr /i "SCRNSAVE.EXE"') do (
    set SCRNSAVE_EXE_EXISTS=1
    if not "%%b"=="" (
        set SCRNSAVE_SET=1
        set SCRNSAVE_VALUE=%%b
    )
)

:: ScreenSaveActive 및 SCRNSAVE.EXE 존재 여부 확인 후 출력
if %SCRNSAVE_ACTIVE_EXISTS% == 0 (
    echo 미흡
    echo 현재 상태: HKEY_CURRENT_USER\SOFTWARE\Policies\Microsoft\Windows\Control Panel\Desktop 레지스트리 경로에 ScreenSaveActive 값이 존재하지 않습니다.
    echo 조치 방법: Help Desk 문의 또는 AD 재설치 바랍니다.
) else if %SCRNSAVE_EXE_EXISTS% == 0 (
    echo 미흡
    echo 현재 상태: HKEY_CURRENT_USER\Control Panel\Desktop 레지스트리 경로에 SCRNSAVE.EXE 값이 존재하지 않습니다.
    echo 조치 방법: 시작 → 화면보호기 변경 → 화면보호기 클릭 → ons 화면 보호기 설정 및 확인
) else if %Sel5% == 1 (
    echo 미흡
    echo 현재 상태: 화면 보호기 레지스트리값이 잘 못 등록되어 있습니다.
    echo 조치 방법:
    echo 1. 레지스트리 HKEY_CURRENT_USER\SOFTWARE\Policies\Microsoft\Windows\Control Panel\Desktop\ScreenSaveActive 값을 1로 변경 또는
    echo 2. CMD → gpupdate /force 입력.
) else (
    echo 양호
    echo 현재 상태: ONS 화면 보호기가 설정되어 있습니다. ScreenSaveActive 값: %b%, SCRNSAVE.EXE 값: %SCRNSAVE_VALUE%
)