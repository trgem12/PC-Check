@echo off

:: ȭ�� ��ȣ�� ��ȣȭ ���θ� ��Ÿ���� ���� �ʱ�ȭ
set /a Sel5 = 1
set b=0
set SCREENSAVER_SECURE_EXISTS=0

:: ScreenSaverIsSecure �� ���� ���� Ȯ��
for /f "tokens=2* delims= " %%a in ('reg query "HKEY_CURRENT_USER\SOFTWARE\Policies\Microsoft\Windows\Control Panel\Desktop" ^| findstr /i "ScreenSaverIsSecure"') do (
    set SCREENSAVER_SECURE_EXISTS=1
    set b=%%b
    if "%%b" == "1" (
        set /a Sel5 = 0
        echo ��ȣ
        echo ���� ����: ȭ�� ��ȣ�Ⱑ ��ȣȭ�Ǿ� �ֽ��ϴ�. ScreenSaverIsSecure ��: %%b
    )
)

:: ScreenSaverIsSecure �� ���� ���� Ȯ�� �� ���
if %SCREENSAVER_SECURE_EXISTS% == 0 (
    echo ����
    echo ���� ����: ������Ʈ�� HKEY_CURRENT_USER\SOFTWARE\Policies\Microsoft\Windows\Control Panel\Desktop ��ο� ScreenSaverIsSecure ���� �������� �ʽ��ϴ�.
    echo ��ġ ���: Help Desk ���� �Ǵ� AD �缳ġ �ٶ��ϴ�.
) else if %Sel5% == 1 (
    echo ����
    echo ���� ����: ȭ�� ��ȣ�Ⱑ ��ȣȭ�Ǿ� ���� �ʽ��ϴ�. ScreenSaverIsSecure ��: %b%
    echo ��ġ ���:
    echo 1. ������Ʈ�� HKEY_CURRENT_USER\SOFTWARE\Policies\Microsoft\Windows\Control Panel\Desktop\ScreenSaverIsSecure ���� 1�� ���� �Ǵ�
    echo 2. CMD �� gpupdate /force �Է�.
)