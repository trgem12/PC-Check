@echo off
setlocal enabledelayedexpansion

:: Script to check shared folders on a Windows 10 PC

:: Variable to store non-conforming shared folder names
set "nonConformingShares="

:: Iterate through the list of shared folders, filtering out irrelevant lines
for /f "tokens=1" %%i in ('net share ^| findstr /R /C:"^[A-Z].*[ ]*$"') do (
    set "share=%%i"
    :: Check if the share does not end with '$'
    if not "!share:~-1!"=="$" (
        set "nonConformingShares=!nonConformingShares! %%i"
    )
)

:: Check if any non-conforming shares were found and output the result
if "!nonConformingShares!"=="" (
    echo ��ȣ
    echo ���� ����: ���� ������ �����ϴ�.
) else (
    echo ����
    echo ���� ����: ���� ������ �����Ǿ� �ֽ��ϴ�. !nonConformingShares!
    echo ��ġ ���: 
    echo 1. �������� Ȯ�� ���� �� ���� �� fsmgmt.msc �Է�
    echo 2. ���ʿ��� ���� ���� Ȯ�� �� �ش� ���� ���� ��Ŭ�� �� ���� ����
    echo 3. cmd �� net share [������ ���� ������] /delete�� ���� ó��
)


endlocal
