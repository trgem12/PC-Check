@echo off
SETLOCAL EnableDelayedExpansion

SET "allGood=true"
SET "insufficientItems="

call :checkFirewall "domain"
call :checkFirewall "private"
call :checkFirewall "public"

IF "!allGood!"=="true" (
    echo 양호
    echo 현재 상태: 모든 프로파일의 방화벽이 활성화되어 있습니다.
) ELSE (
    echo 미흡
    echo 현재 상태: !insufficientItems! 방화벽 설정이 꺼져 있습니다.
    echo 조치 방법:
    echo 1. 시작→ 방화벽 및 네트워크 보호 → 도메인,개인,공용 방화벽 활성화 상태 확인
    echo 2. 비활성화되어 있는 네트워크 클릭 →  Microsoft Defender 방화벽 켬
    echo 3. 활성화 되어 있는 경우 CMD 관리자 권한 실행 → netsh advfirewall set allprofiles state on 입력 후 재점검 시행
)


exit /b

:checkFirewall
FOR /F "tokens=*" %%i IN ('netsh advfirewall show %1profile ^| findstr /C:"상태"') DO (
    SET status=%%i
    SET status=!status:상태=!
    SET status=!status: =!
    IF NOT "!status!"=="사용" (
        SET "allGood=false"
        IF NOT "!insufficientItems!"=="" SET insufficientItems=!insufficientItems!,
        SET insufficientItems=!insufficientItems!%1
    )
)
exit /b