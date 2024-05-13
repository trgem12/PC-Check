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
        echo ��ȣ
        echo ���� ����: �ֽ� �������� ����Ǿ� �ֽ��ϴ�. DisplayVersion: %DisplayVersion%
    ) else (
        echo ����
        echo ���� ����: �ֽ� �������� ����Ǿ� ���� �ʽ��ϴ�. ���׷��̵尡 �ʿ��մϴ�.  DisplayVersion: %DisplayVersion%
        echo ��ġ ���: MS�� ���� ����Ʈ ���� �� ���׷��̵� ����

    )
) else (
    echo ����
    echo ���� ����: �ֽ� �������� ����Ǿ� ���� �ʽ��ϴ�. ���׷��̵尡 �ʿ��մϴ�.  DisplayVersion: %DisplayVersion%
    echo ��ġ ���: MS�� ���� ����Ʈ ���� �� ���׷��̵� ����
)
