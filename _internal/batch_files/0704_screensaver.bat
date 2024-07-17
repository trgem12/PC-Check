@echo off

:: Initialize the variable to indicate screensaver not set
set /a Sel5 = 1
set b=0

:: Check the registry for ScreenSaveActive setting
for /f "tokens=2* delims= " %%a in ('reg query "HKEY_CURRENT_USER\SOFTWARE\Policies\Microsoft\Windows\Control Panel\Desktop" ^| findstr /i "ScreenSaveActive"') do (
    if "%%b" == "1" (
        set /a Sel5 = 0
        set b=%%b
    )
)

:: Check the registry for SCRNSAVE.EXE setting
set SCRNSAVE_SET=0
for /f "tokens=2* delims= " %%a in ('reg query "HKEY_CURRENT_USER\Control Panel\Desktop" ^| findstr /i "SCRNSAVE.EXE"') do (
    if not "%%b"=="" (
        set SCRNSAVE_SET=1
    )
)

:: Check if screensaver is not set or SCRNSAVE.EXE is not set and display message
if %Sel5% == 1 (
    echo ����
    echo ���� ����: ȭ�� ��ȣ�� ������ �Ǿ� ���� �ʽ��ϴ�.
    echo ��ġ ���: Help Desk�� ȭ�麸ȣ�� ���� ���� ���� �ٶ��ϴ�.
) else if %SCRNSAVE_SET% == 0 (
    echo ����
    echo ���� ����: SCRNSAVE.EXE ���� �����Ǿ� ���� �ʽ��ϴ�.
    echo ��ġ ���: ȭ�麸ȣ�� ���� �� ȭ�麸ȣ�� ���� �� Ȯ�� Ŭ��
) else (
    echo ��ȣ
    echo ���� ����: ȭ�� ��ȣ�Ⱑ �����Ǿ� �ֽ��ϴ�. ScreenSaveActive ��: %b%
)