@echo off
setlocal enabledelayedexpansion

REM �ּ� ��й�ȣ ���� Ȯ��
for /f "tokens=2 delims=:" %%a in ('net accounts ^| findstr /C:"�ּ� ��ȣ ����"') do (
    set minLength=%%a
)

REM ��� ���
set /a minLength=!minLength:~1!
if !minLength! GEQ 8 (
    echo ��ȣ
    echo ���� ����: ���� ��й�ȣ ���� ���� !minLength!���Դϴ�.
) else (
    echo ����
    echo ���� ����: �ּ� ��й�ȣ ���̰� 8�� �̸��Դϴ�. ���� ��й�ȣ ���� ���� !minLength!���Դϴ�.
    echo ��ġ ���: SKT AD�� ���� ����Ǵ� �κ����� AD �缳ġ�� �ʿ��մϴ�.
)


endlocal
