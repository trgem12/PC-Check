@echo off

:: Define the target OS versions and Display Versions
set "TargetVersionStart1=10.0"
set "TargetDisplayVersion1=22H2"
set "TargetDisplayVersion2=23H2"
set "TargetVersionStart2=11.0"

:: Get the OS version using WMIC
for /f "tokens=2 delims==" %%a in ('wmic os get Version /value') do set "OSVersion=%%a"
:: Trim whitespace from OSVersion
set "OSVersion=%OSVersion: =%"

:: Get the DisplayVersion from the registry
for /f "tokens=2,*" %%b in ('reg query "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion" /v DisplayVersion') do set "DisplayVersion=%%c"

:: Check if the OS version and DisplayVersion match the target
if "%OSVersion%" geq "%TargetVersionStart1%" (
    if "%DisplayVersion%"=="%TargetDisplayVersion1%" (
        echo 양호
        echo 현재 상태: 최신 서비스팩이 적용되어 있습니다. Windowsversion: %OSVersion% DisplayVersion: %DisplayVersion%
    ) else if "%DisplayVersion%"=="%TargetDisplayVersion2%" (
        echo 양호
        echo 현재 상태: 최신 서비스팩이 적용되어 있습니다. Windowsversion: %OSVersion% DisplayVersion: %DisplayVersion%
    ) else (
        echo 미흡
        echo 현재 상태: 최신 서비스팩이 적용되어 있지 않습니다. 업그레이드가 필요합니다. Windowsversion: %OSVersion% DisplayVersion: %DisplayVersion%
        echo 조치 방법: MS社 공식 사이트 접속 후 업그레이드 시행
    )
) else if "%OSVersion%" geq "%TargetVersionStart2%" (
    if "%DisplayVersion%"=="%TargetDisplayVersion1%" (
        echo 양호
        echo 현재 상태: 최신 서비스팩이 적용되어 있습니다. Windowsversion: %OSVersion% DisplayVersion: %DisplayVersion%
    ) else if "%DisplayVersion%"=="%TargetDisplayVersion2%" (
        echo 양호
        echo 현재 상태: 최신 서비스팩이 적용되어 있습니다. Windowsversion: %OSVersion% DisplayVersion: %DisplayVersion%
    ) else (
        echo 미흡
        echo 현재 상태: 최신 서비스팩이 적용되어 있지 않습니다. 업그레이드가 필요합니다.  Windowsversion: %OSVersion% DisplayVersion: %DisplayVersion%
        echo 조치 방법: MS社 공식 사이트 접속 후 업그레이드 시행
    )
) else (
    echo 미흡
    echo 현재 상태: 최신 서비스팩이 적용되어 있지 않습니다. 업그레이드가 필요합니다. Windowsversion: %OSVersion% DisplayVersion: %DisplayVersion%
    echo 조치 방법: MS社 공식 사이트 접속 후 업그레이드 시행
)