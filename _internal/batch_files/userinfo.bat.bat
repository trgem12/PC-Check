@echo off
setlocal enabledelayedexpansion

REM 호스트네임에서 4번째부터 10번째 문자 추출
for /f "tokens=*" %%a in ('hostname') do set hostname=%%a
set accountName=!hostname:~3,7!

REM 사용자 정보 확인용
for /f "tokens=3*" %%a in ('net user !accountName! /DOMAIN ^| findstr /C:"전체 이름"') do (
    set "user_info=%%a %%b"
)
REM _SK오앤에스 부분 삭제
set "user_info=!user_info:_SK오앤에스=!"

echo %user_info%

