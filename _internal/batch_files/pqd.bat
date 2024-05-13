@echo off

set SCRNSAVE_KEY="HKEY_CURRENT_USER\Control Panel\Desktop"
set SCRNSAVE_VALUE="SCRNSAVE.EXE"

for /f "tokens=2* delims= " %%a in ('reg query %SCRNSAVE_KEY% /v %SCRNSAVE_VALUE%') do (
    set SCRNSAVE_PATH=%%b
)

if not defined SCRNSAVE_PATH (
    echo 양호
    echo 현재 상태: 화면보호기가 설정되어 있습니다.
) else (
    echo 미흡
    echo 현재 상태: 화면보호기가 설정되어 있지 않습니다. 
    echo 조치 방법: SKT AD를 통해 제어되는 부분으로 AD 재설치가 필요합니다. 
)