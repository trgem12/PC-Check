@echo off
setlocal EnableDelayedExpansion

:: ScreenSaveTimeOut ���� �ִ��� Ȯ��
set ScreenSaveTimeOutExists=0
for /f "tokens=2*" %%a in ('reg query "HKEY_CURRENT_USER\SOFTWARE\Policies\Microsoft\Windows\Control Panel\Desktop" /v ScreenSaveTimeOut 2^>nul') do (
    set ScreenSaveTimeOutExists=1
    set ScreenSaverTimeSec=%%b
)

:: ScreenSaveTimeOut ���� �����ϴ��� Ȯ��
if %ScreenSaveTimeOutExists% == 0 (
    echo ����
    echo ���� ����: HKEY_CURRENT_USER\SOFTWARE\Policies\Microsoft\Windows\Control Panel\Desktop ������Ʈ�� ��ο� ScreenSaveTimeOut ���� �������� �ʽ��ϴ�.
    echo ��ġ ���: Help Desk ���� �Ǵ� AD �缳ġ �ٶ��ϴ�.
    goto endScript
)

:: ScreenSaverTimeSec ���� 600�� �̻����� Ȯ��
if !ScreenSaverTimeSec! geq 600 (
    echo ��ȣ
    echo ���� ����: ȭ�� ��ȣ�Ⱑ !ScreenSaverTimeSec! �ʷ� �����Ǿ� �ֽ��ϴ�.
) else (
    echo ����
    echo ���� ����: ȭ�� ��ȣ�� ���� �ð��� !ScreenSaverTimeSec! �ʷ� �����Ǿ� �ֽ��ϴ�. 600�ʷ� ������ �ʿ��մϴ�.
    echo ��ġ ���: 
    echo 1. ������Ʈ�� \HKEY_CURRENT_USER\SOFTWARE\Policies\Microsoft\Windows\Control Panel\Desktop\ScreenSaveTimeOut ���� 600���� ���� �Ǵ�
    echo 2. CMD �� gpupdate /force �Է�.
)

:endScript
endlocal