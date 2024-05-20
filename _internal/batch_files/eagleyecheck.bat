@echo off
setlocal

rem 확인할 프로그램의 설치 경로
set program_path="C:\iEC\iECUI.exe"

rem 프로그램 파일이 존재하는지 확인
if exist %program_path% (
    echo 양호
    echo 현재 상태: 이글아이 설치되어 있습니다.
) else (
    echo 미흡
    echo 현재 상태: 이글아이 미설치되어 있습니다. 
    echo 조치 방법: i-net→sk ons store→PC Tab→이글아이 다운로드 및 설치 
)

endlocal
rem pause
