@echo off
setlocal

REM ���� ������ ���Ϸ� ��������
secedit /export /cfg tempcfg.ini >nul 2>&1

REM ��й�ȣ ���⼺ �䱸 ���� Ȯ��
type tempcfg.ini | findstr /C:"PasswordComplexity = 1" >nul
if %errorlevel%==0 (
    echo ��ȣ
    echo ���� ����: ��й�ȣ ���⼺ �䱸 ���� ���Դϴ�.
) else (
    echo ����
    echo ���� ����: ���� ��й�ȣ ���⼺ �䱸 ������ �̻������ �Ǿ� �ֽ��ϴ�.
    echo ��ġ ���: SKT AD�� ���� ����Ǵ� �κ����� AD �缳ġ�� �ʿ��մϴ�.
)

REM �ӽ� ���� ���� (�ʿ��� ��� �� ���� �ּ� ó���ϰų� �����ϼ���)
del tempcfg.ini >nul

endlocal