@echo off
setlocal enabledelayedexpansion

REM 최소 비밀번호 길이 확인
for /f "tokens=2 delims=:" %%a in ('net accounts ^| findstr /C:"최소 암호 길이"') do (
    set minLength=%%a
)

REM 결과 출력
set /a minLength=!minLength:~1!
if !minLength! GEQ 8 (
    echo 양호
    echo 현재 상태: 현재 비밀번호 설정 값은 !minLength!자입니다.
) else (
    echo 미흡
    echo 현재 상태: 최소 비밀번호 길이가 8자 미만입니다. 현재 비밀번호 설정 값은 !minLength!자입니다.
    echo 조치 방법: SKT AD를 통해 제어되는 부분으로 AD 재설치가 필요합니다.
)


endlocal
