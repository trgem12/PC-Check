@echo off

:: 화면 보호기 암호화 여부를 나타내는 변수 초기화
set /a Sel5 = 1
set b=0
set SCREENSAVER_SECURE_EXISTS=0

:: ScreenSaverIsSecure 값 존재 여부 확인
for /f "tokens=2* delims= " %%a in ('reg query "HKEY_CURRENT_USER\SOFTWARE\Policies\Microsoft\Windows\Control Panel\Desktop" ^| findstr /i "ScreenSaverIsSecure"') do (
    set SCREENSAVER_SECURE_EXISTS=1
    set b=%%b
    if "%%b" == "1" (
        set /a Sel5 = 0
        echo 양호
        echo 현재 상태: 화면 보호기가 암호화되어 있습니다. ScreenSaverIsSecure 값: %%b
    )
)

:: ScreenSaverIsSecure 값 존재 여부 확인 후 출력
if %SCREENSAVER_SECURE_EXISTS% == 0 (
    echo 미흡
    echo 현재 상태: 레지스트리 HKEY_CURRENT_USER\SOFTWARE\Policies\Microsoft\Windows\Control Panel\Desktop 경로에 ScreenSaverIsSecure 값이 존재하지 않습니다.
    echo 조치 방법: Help Desk 문의 또는 AD 재설치 바랍니다.
) else if %Sel5% == 1 (
    echo 미흡
    echo 현재 상태: 화면 보호기가 암호화되어 있지 않습니다. ScreenSaverIsSecure 값: %b%
    echo 조치 방법:
    echo 1. 레지스트리 HKEY_CURRENT_USER\SOFTWARE\Policies\Microsoft\Windows\Control Panel\Desktop\ScreenSaverIsSecure 값을 1로 변경 또는
    echo 2. CMD → gpupdate /force 입력.
)