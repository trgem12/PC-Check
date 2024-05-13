@echo off
setlocal

REM 보안 설정을 파일로 내보내기
secedit /export /cfg tempcfg.ini >nul 2>&1

REM '복구 콘솔 자동 로그온 허용' 상태 확인
type tempcfg.ini | findstr /C:"RecoveryConsole: Allow automatic administrative logon" >nul
if %errorlevel%==0 (
    echo 미흡
    echo 현재상태: 복구 콘솔 자동 로그온 허용이 활성화되어 있습니다.
    echo 조치방법: 제어판→관리도구→로컬보안정책→보안설정→로컬정책→보안옵션→복구콘솔:자동관리로그온허용속성'사용 안 함'으로 설정
) else (
    echo 양호
    echo 현재상태: '복구 콘솔 자동 로그온 허용'이 비활성화되어 있습니다.
)

REM 임시 파일 삭제
del tempcfg.ini >nul

endlocal

