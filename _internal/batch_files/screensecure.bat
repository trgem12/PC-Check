@echo off

:: Initialize the variable to indicate screensaver not set
set /a Sel5 = 1
set b=0

:: Check the registry for ScreenSaverIsSecure setting
for /f "tokens=2* delims= " %%a in ('reg query "HKEY_CURRENT_USER\SOFTWARE\Policies\Microsoft\Windows\Control Panel\Desktop" ^| findstr /i "ScreenSaverIsSecure"') do (
    set b=%%b
    if "%%b" == "1" (
        set /a Sel5 = 0
        echo ��ȣ
        echo ���� ����: ȭ�� ��ȣ�Ⱑ ��ȣȭ�Ǿ� �ֽ��ϴ�. ScreenSaverIsSecure ��: %%b
    )
)

:: Check if screensaver is not set and display message
if %Sel5% == 1 (
    echo ����
    echo ���� ����: ȭ�� ��ȣ�Ⱑ ��ȣȭ�Ǿ� ���� �ʽ��ϴ�. ScreenSaverIsSecure ��: %b%
    echo ��ġ ���: Help Desk�� ȭ�麸ȣ�� ���� ���� �ٶ��ϴ�.
)