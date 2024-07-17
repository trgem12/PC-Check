@echo off
setlocal

REM 보안 설정을 파일로 내보내기
secedit /export /cfg tempcfg.ini >nul 2>&1

REM 비밀번호 복잡성 요구 사항 확인
type tempcfg.ini | findstr /C:"PasswordComplexity = 1" >nul
if %errorlevel%==0 (
    echo 양호
    echo 현재 상태: 비밀번호 복잡성 요구 충족 중입니다.
) else (
    echo 미흡
    echo 현재 상태: 현재 비밀번호 복잡성 요구 사항이 미사용으로 되어 있습니다.
    echo 조치 방법: SKT AD를 통해 제어되는 부분으로 AD 재설치가 필요합니다.
)

REM 임시 파일 삭제 (필요한 경우 이 줄을 주석 처리하거나 삭제하세요)
del tempcfg.ini >nul

endlocal