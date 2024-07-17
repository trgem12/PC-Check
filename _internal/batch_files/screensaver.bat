@echo off

:: ���� �ʱ�ȭ
set /a Sel5 = 1
set b=0
set SCRNSAVE_VALUE=""
set SCRNSAVE_ACTIVE_EXISTS=0
set SCRNSAVE_EXE_EXISTS=0

:: ScreenSaveActive ���� ���� Ȯ��
for /f "tokens=2* delims= " %%a in ('reg query "HKEY_CURRENT_USER\SOFTWARE\Policies\Microsoft\Windows\Control Panel\Desktop" ^| findstr /i "ScreenSaveActive"') do (
    set SCRNSAVE_ACTIVE_EXISTS=1
    if "%%b" == "1" (
        set /a Sel5 = 0
        set b=%%b
    )
)

REM HKEY_CURRENT_USER\SOFTWARE\Policies\Microsoft\Windows\Control Panel\Desktop

:: SCRNSAVE.EXE ���� ���� Ȯ��
for /f "tokens=2* delims= " %%a in ('reg query "HKEY_CURRENT_USER\Control Panel\Desktop" ^| findstr /i "SCRNSAVE.EXE"') do (
    set SCRNSAVE_EXE_EXISTS=1
    if not "%%b"=="" (
        set SCRNSAVE_SET=1
        set SCRNSAVE_VALUE=%%b
    )
)

:: ScreenSaveActive �� SCRNSAVE.EXE ���� ���� Ȯ�� �� ���
if %SCRNSAVE_ACTIVE_EXISTS% == 0 (
    echo ����
    echo ���� ����: HKEY_CURRENT_USER\SOFTWARE\Policies\Microsoft\Windows\Control Panel\Desktop ������Ʈ�� ��ο� ScreenSaveActive ���� �������� �ʽ��ϴ�.
    echo ��ġ ���: Help Desk ���� �Ǵ� AD �缳ġ �ٶ��ϴ�.
) else if %SCRNSAVE_EXE_EXISTS% == 0 (
    echo ����
    echo ���� ����: HKEY_CURRENT_USER\Control Panel\Desktop ������Ʈ�� ��ο� SCRNSAVE.EXE ���� �������� �ʽ��ϴ�.
    echo ��ġ ���: ���� �� ȭ�麸ȣ�� ���� �� ȭ�麸ȣ�� Ŭ�� �� ons ȭ�� ��ȣ�� ���� �� Ȯ��
) else if %Sel5% == 1 (
    echo ����
    echo ���� ����: ȭ�� ��ȣ�� ������Ʈ������ �� �� ��ϵǾ� �ֽ��ϴ�.
    echo ��ġ ���:
    echo 1. ������Ʈ�� HKEY_CURRENT_USER\SOFTWARE\Policies\Microsoft\Windows\Control Panel\Desktop\ScreenSaveActive ���� 1�� ���� �Ǵ�
    echo 2. CMD �� gpupdate /force �Է�.
) else (
    echo ��ȣ
    echo ���� ����: ONS ȭ�� ��ȣ�Ⱑ �����Ǿ� �ֽ��ϴ�. ScreenSaveActive ��: %b%, SCRNSAVE.EXE ��: %SCRNSAVE_VALUE%
)