@echo off
setlocal

rem 파일 경로 설정
set file_path=C:\Program Files (x86)\evEraser_Win\evEraser.exe

rem 파일 존재 여부 확인
if exist "%file_path%" (
    echo 양호
    echo 현재 상태: evEraser 설치되어 있습니다. 
) else (
    echo 미흡
    echo 현재 상태: evEraser 미설치되어 있습니다. 
    echo 조치 방법: SKT AD 설치 후 업무망 접속되어 있으면 자동 설치되나 문제가 있는 경우 Help Desk 문의 바랍니다.
)

endlocal
rem pause