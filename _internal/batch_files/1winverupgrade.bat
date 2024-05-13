@echo off

:: Define the target OS version and Display Version
set "TargetVersionStart=10.0"
set "TargetDisplayVersion=22H2"

:: Get the OS version using WMIC
for /f "tokens=2 delims==" %%a in ('wmic os get Version /value') do set "OSVersion=%%a"
:: Trim whitespace from OSVersion
set "OSVersion=%OSVersion: =%"

:: Get the DisplayVersion from the registry
for /f "tokens=2,*" %%b in ('reg query "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion" /v DisplayVersion') do set "DisplayVersion=%%c"

:: Echo the detected OSVersion and DisplayVersion for debugging
:: echo Detected OSVersion: %OSVersion%
:: echo Detected DisplayVersion: %DisplayVersion%

:: Check if the OS version and DisplayVersion match the target
if "%OSVersion%" geq "%TargetVersionStart%" (
    if "%DisplayVersion%"=="%TargetDisplayVersion%" (
        echo 양호
        echo 현재 상태: 최신 서비스팩이 적용되어 있습니다. DisplayVersion: %DisplayVersion%
    ) else (
        echo 미흡
        echo 현재 상태: 최신 서비스팩이 적용되어 있지 않습니다. 업그레이드가 필요합니다.  DisplayVersion: %DisplayVersion%
        echo 조치 방법: MS社 공식 사이트 접속 후 업그레이드 시행

    )
) else (
    echo 미흡
    echo 현재 상태: 최신 서비스팩이 적용되어 있지 않습니다. 업그레이드가 필요합니다.  DisplayVersion: %DisplayVersion%
    echo 조치 방법: MS社 공식 사이트 접속 후 업그레이드 시행
)
