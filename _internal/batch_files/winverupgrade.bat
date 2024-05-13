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
        echo ��ȣ
        echo ���� ����: �ֽ� �������� ����Ǿ� �ֽ��ϴ�. Windowsversion: %OSVersion% DisplayVersion: %DisplayVersion%
    ) else if "%DisplayVersion%"=="%TargetDisplayVersion2%" (
        echo ��ȣ
        echo ���� ����: �ֽ� �������� ����Ǿ� �ֽ��ϴ�. Windowsversion: %OSVersion% DisplayVersion: %DisplayVersion%
    ) else (
        echo ����
        echo ���� ����: �ֽ� �������� ����Ǿ� ���� �ʽ��ϴ�. ���׷��̵尡 �ʿ��մϴ�. Windowsversion: %OSVersion% DisplayVersion: %DisplayVersion%
        echo ��ġ ���: MS�� ���� ����Ʈ ���� �� ���׷��̵� ����
    )
) else if "%OSVersion%" geq "%TargetVersionStart2%" (
    if "%DisplayVersion%"=="%TargetDisplayVersion1%" (
        echo ��ȣ
        echo ���� ����: �ֽ� �������� ����Ǿ� �ֽ��ϴ�. Windowsversion: %OSVersion% DisplayVersion: %DisplayVersion%
    ) else if "%DisplayVersion%"=="%TargetDisplayVersion2%" (
        echo ��ȣ
        echo ���� ����: �ֽ� �������� ����Ǿ� �ֽ��ϴ�. Windowsversion: %OSVersion% DisplayVersion: %DisplayVersion%
    ) else (
        echo ����
        echo ���� ����: �ֽ� �������� ����Ǿ� ���� �ʽ��ϴ�. ���׷��̵尡 �ʿ��մϴ�.  Windowsversion: %OSVersion% DisplayVersion: %DisplayVersion%
        echo ��ġ ���: MS�� ���� ����Ʈ ���� �� ���׷��̵� ����
    )
) else (
    echo ����
    echo ���� ����: �ֽ� �������� ����Ǿ� ���� �ʽ��ϴ�. ���׷��̵尡 �ʿ��մϴ�. Windowsversion: %OSVersion% DisplayVersion: %DisplayVersion%
    echo ��ġ ���: MS�� ���� ����Ʈ ���� �� ���׷��̵� ����
)