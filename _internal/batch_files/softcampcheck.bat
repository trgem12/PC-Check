@echo off
setlocal

rem 확인할 프로그램 파일 경로
set program_path="C:\Windows\Softcamp\SDS\SDSHlpr.exe"

rem 프로그램 파일이 존재하는지 확인
if exist "%program_path%" (
    echo 양호
    echo 현재상태: 문서보안 설치되어 있습니다. 
) else (
    echo 미흡
    echo 현재상태: 문서보안 미설치되어 있습니다. 
    echo 조치방법: i-net→sk ons store→문서보안 다운로드 및 설치 
)

endlocal
rem pause