@echo off
setlocal enabledelayedexpansion

REM 호스트네임에서 4번째부터 10번째 문자 추출
for /f "tokens=*" %%a in ('hostname') do set hostname=%%a
set accountName=!hostname:~3,7!

REM 도메인 계정의 마지막 비밀번호 설정 날짜 확인
for /f "tokens=5*" %%a in ('net user !accountName! /DOMAIN ^| findstr /C:"마지막으로 암호 설정한 날짜"') do set lastPwdDate=%%a

REM lastPwdDate를 비교 가능한 형식 (YYYY-MM-DD)으로 변환
set formattedLastPwdDate=!lastPwdDate:~0,4!-!lastPwdDate:~5,2!-!lastPwdDate:~8,2!
REM echo !formattedLastPwdDate!

REM 현재 날짜를 찾고 비교 가능한 형식 (YYYY-MM-DD)으로 변환
REM %date%의 출력 형식이 YYYY-MM-DD 라고 가정
set formattedCurrentDate=%date%
REM echo !formattedCurrentDate!

REM 날짜 차이를 일수로 계산
for /f %%a in ('powershell -Command "(New-TimeSpan -Start !formattedLastPwdDate! -End !formattedCurrentDate!).Days"') do set dateDiff=%%a

REM 비교하고 출력
if !dateDiff! gtr 90 (
    echo 미흡
    echo 현재 상태: PW를 !dateDiff!일 동안 변경하지 않았습니다.
    echo 조치 방법: Ctrl+Alt+Del을 누른 다음[암호 변경]을 선택 후 PW 변경
) else (
    echo 양호
    echo 현재 상태: PW 변경 !dateDiff!일 입니다.
)

endlocal