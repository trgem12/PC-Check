@echo off
setlocal enabledelayedexpansion

REM ȣ��Ʈ���ӿ��� 4��°���� 10��° ���� ����
for /f "tokens=*" %%a in ('hostname') do set hostname=%%a
set accountName=!hostname:~3,7!

REM ����� ���� Ȯ�ο�
for /f "tokens=3*" %%a in ('net user !accountName! /DOMAIN ^| findstr /C:"��ü �̸�"') do (
    set "user_info=%%a %%b"
)
REM _SK���ؿ��� �κ� ����
set "user_info=!user_info:_SK���ؿ���=!"

echo %user_info%

