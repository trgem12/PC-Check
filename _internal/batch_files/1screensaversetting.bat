@echo off
setlocal EnableDelayedExpansion

:: Retrieve the screensaver timeout setting in seconds from the registry
for /f "tokens=2*" %%a in ('reg query "HKEY_CURRENT_USER\Control Panel\Desktop" /v ScreenSaveTimeOut') do set ScreenSaverTimeSec=%%b

:: Convert the timeout from seconds to minutes
set /a ScreenSaverTimeMin=!ScreenSaverTimeSec! / 60

:: Check if the screensaver timeout is 10 minutes or more
if !ScreenSaverTimeMin! geq 10 (
    echo ��ȣ
    echo ���� ����: ȭ�� ��ȣ�� !ScreenSaverTimeMin! �� ���� ��
    goto endScript
)

:: If the above condition is not met, this part will execute
echo ����
echo ���� ����: ȭ�� ��ȣ�� ���� �ð��� !ScreenSaverTimeMin! ������ ���� �ʿ�
echo ��ġ ���: SKT AD�� ���� ����Ǵ� �κ����� AD �缳ġ�� �ʿ��մϴ�.

:endScript
endlocal

