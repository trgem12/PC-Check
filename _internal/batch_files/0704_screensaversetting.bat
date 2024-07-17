@echo off
setlocal EnableDelayedExpansion

:: Retrieve the screensaver timeout setting in seconds from the registry
for /f "tokens=2*" %%a in ('reg query "HKEY_CURRENT_USER\SOFTWARE\Policies\Microsoft\Windows\Control Panel\Desktop" /v ScreenSaveTimeOut') do set ScreenSaverTimeSec=%%b

:: Check if the screensaver timeout is 600 seconds or more
if !ScreenSaverTimeSec! geq 600 (
    echo ��ȣ
    echo ���� ����: ȭ�� ��ȣ�� !ScreenSaverTimeSec! �� ���� ��
    goto endScript
)

:: If the above condition is not met, this part will execute
echo ����
echo ���� ����: ȭ�� ��ȣ�� ���� �ð��� !ScreenSaverTimeSec! �ʷ� ���� �ʿ��մϴ�.
echo ��ġ ���: ȭ�� ��ȣ�� ���� �ð� ���� ������ Help Desk ���� �ٶ��ϴ�.

:endScript
endlocal

pause