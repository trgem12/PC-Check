@echo off

:: ���� �ʱ�ȭ
set /a Sel5 = 1
set b=0
set SCRNSAVE_VALUE=""

:: ScreenSaveActive ���� ���� Ȯ��
for /f "tokens=2* delims= " %%a in ('reg query "HKEY_CURRENT_USER\SOFTWARE\Policies\Microsoft\Windows\Control Panel\Desktop" ^| findstr /i "ScreenSaveActive"') do (
    if "%%b" == "1" (
        set /a Sel5 = 0
        set b=%%b
    )
)

REM HKEY_CURRENT_USER\SOFTWARE\Policies\Microsoft\Windows\Control Panel\Desktop

:: SCRNSAVE.EXE ���� ���� Ȯ��
set SCRNSAVE_SET=0
for /f "tokens=2* delims= " %%a in ('reg query "HKEY_CURRENT_USER\Control Panel\Desktop" ^| findstr /i "SCRNSAVE.EXE"') do (
    if not "%%b"=="" (
        set SCRNSAVE_SET=1
        set SCRNSAVE_VALUE=%%b
    )
)

:: ScreenSaveActive �� SCRNSAVE.EXE ���� ���� Ȯ�� �� ���
if %Sel5% == 1 (
    echo ����
    echo ���� ����: ȭ�� ��ȣ�� ������ �Ǿ� ���� �ʽ��ϴ�.
    echo ��ġ ���:
    echo 1. ������Ʈ�� HKEY_CURRENT_USER\SOFTWARE\Policies\Microsoft\Windows\Control Panel\Desktop\ScreenSaveActive ���� 1�� �������ּ���.
    echo 2. ������Ʈ�� ���� ���ٸ� Help Desk ���� �� ȭ�� ��ȣ�� �缳�� �ٶ��ϴ�.
) else if %SCRNSAVE_SET% == 0 (
    echo ����
    echo ���� ����: SCRNSAVE.EXE ���� �����Ǿ� ���� �ʽ��ϴ�.
    echo ��ġ ���: ȭ�麸ȣ�� ���� �� OSN ȭ�麸ȣ�� Ŭ�� �� Ȯ��
) else (
    echo ��ȣ
    echo ���� ����: ONS ȭ�� ��ȣ�Ⱑ �����Ǿ� �ֽ��ϴ�. ScreenSaveActive ��: %b%, SCRNSAVE.EXE ��: %SCRNSAVE_VALUE%
)