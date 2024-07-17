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
    echo 1. ���ۡ� ��ȭ�� �� ��Ʈ��ũ ��ȣ �� ������,����,���� ��ȭ�� Ȱ��ȭ ���� Ȯ��
    echo 2. ��Ȱ��ȭ�Ǿ� �ִ� ��Ʈ��ũ Ŭ�� ��  Microsoft Defender ��ȭ�� ��
    echo 3. Ȱ��ȭ �Ǿ� �ִ� ��� CMD ������ ���� ���� �� netsh advfirewall set allprofiles state on �Է� �� ������ ����
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