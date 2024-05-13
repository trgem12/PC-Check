@echo off
SETLOCAL EnableDelayedExpansion

SET "allGood=true"
SET "insufficientItems="

call :checkFirewall "domain"
call :checkFirewall "private"
call :checkFirewall "public"

IF "!allGood!"=="true" (
    echo ��ȣ
    echo ���� ����: ��� ���������� ��ȭ���� Ȱ��ȭ�Ǿ� �ֽ��ϴ�.
) ELSE (
    echo ����
    echo ���� ����: !insufficientItems! ��ȭ�� ������ ���� �ֽ��ϴ�.
    echo ��ġ ���:
    echo 1. ���ۡ� ��ȭ�� �� ��Ʈ��ũ ��ȣ �� ��ȭ�� Ȱ��ȭ
    echo 2. ��Ȱ��ȭ�Ǿ� �ִ� ��Ʈ��ũ Ŭ�� ��  Microsoft Defender ��ȭ�� ��
    echo 3. �� �������� ��ġ�� �ȵǴ� ��� Help Desk ���� �ٶ��ϴ�.
)


exit /b

:checkFirewall
FOR /F "tokens=*" %%i IN ('netsh advfirewall show %1profile ^| findstr /C:"����"') DO (
    SET status=%%i
    SET status=!status:����=!
    SET status=!status: =!
    IF NOT "!status!"=="���" (
        SET "allGood=false"
        IF NOT "!insufficientItems!"=="" SET insufficientItems=!insufficientItems!,
        SET insufficientItems=!insufficientItems!%1
    )
)
exit /b