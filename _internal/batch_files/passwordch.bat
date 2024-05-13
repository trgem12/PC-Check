@echo off
setlocal enabledelayedexpansion

REM ȣ��Ʈ���ӿ��� 4��°���� 10��° ���� ����
for /f "tokens=*" %%a in ('hostname') do set hostname=%%a
set accountName=!hostname:~3,7!

REM ������ ������ ������ ��й�ȣ ���� ��¥ Ȯ��
for /f "tokens=5*" %%a in ('net user !accountName! /DOMAIN ^| findstr /C:"���������� ��ȣ ������ ��¥"') do set lastPwdDate=%%a

REM lastPwdDate�� �� ������ ���� (YYYY-MM-DD)���� ��ȯ
set formattedLastPwdDate=!lastPwdDate:~0,4!-!lastPwdDate:~5,2!-!lastPwdDate:~8,2!
REM echo !formattedLastPwdDate!

REM ���� ��¥�� ã�� �� ������ ���� (YYYY-MM-DD)���� ��ȯ
REM %date%�� ��� ������ YYYY-MM-DD ��� ����
set formattedCurrentDate=%date%
REM echo !formattedCurrentDate!

REM ��¥ ���̸� �ϼ��� ���
for /f %%a in ('powershell -Command "(New-TimeSpan -Start !formattedLastPwdDate! -End !formattedCurrentDate!).Days"') do set dateDiff=%%a

REM ���ϰ� ���
if !dateDiff! gtr 90 (
    echo ����
    echo ���� ����: PW�� !dateDiff!�� ���� �������� �ʾҽ��ϴ�.
    echo ��ġ ���: Ctrl+Alt+Del�� ���� ����[��ȣ ����]�� ���� �� PW ����
) else (
    echo ��ȣ
    echo ���� ����: PW ���� !dateDiff!�� �Դϴ�.
)

endlocal