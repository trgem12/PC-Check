@echo off

:: Initialize the variable to indicate screensaver not set
set /a Sel5 = 1

:: Check the registry for SCRNSAVE.EXE setting
for /f "tokens=2* delims= " %%a in ('reg query "HKEY_CURRENT_USER\Control Panel\Desktop" ^| findstr /i "SCRNSAVE.EXE"') do (
    if not "%%b" == "" (
        set /a Sel5 = 0
        echo ��ȣ
        echo ���� ����: %%b ȭ�� ��ȣ�Ⱑ �����Ǿ� �ֽ��ϴ�.
    )
)

:: Check if screensaver is not set and display message
if %Sel5% == 1 (
    echo ����
    echo ���� ����: ȭ�� ��ȣ�� ������ �Ǿ� ���� �ʽ��ϴ�.
    echo ��ġ ���: SKT AD�� ���� ����Ǵ� �κ����� AD �缳ġ�� �ʿ��մϴ�.
)

pause