@echo off
setlocal enabledelayedexpansion

REM bcdedit ��ɾ �����Ͽ� ��Ʈ ��Ʈ���� 'description' ���� �����ɴϴ�.
set "count=0"
for /f "tokens=1* delims=: " %%a in ('bcdedit /enum ^| findstr /c:"Windows 10" /c:"description"') do (
    if "%%a"=="description" (
        if not "%%b"=="Windows Boot Manager" (
            set /a count+=1
            set "os[!count!]=%%b"
        )
    )
)

REM ��Ʈ ��Ʈ���� ���� Ȯ���Ͽ� ����� ����մϴ�.
if !count! equ 1 (
    echo ��ȣ
    echo ���� ����: ���� PC�� !os[1]! �� ��ġ�Ǿ� �ֽ��ϴ�.
) else if !count! gtr 1 (
    echo ����
    for /l %%i in (1, 1, !count!) do (
        echo ���� ����: PC�� 2�� �̻��� OS %%i: !os[%%i]! �� ��ġ�Ǿ� �ֽ��ϴ�.
        echo ��ġ ���: ���ۡ�����msconfig �Է¡�ý��۱��� ���� �ǡ������� �ʴ� OS ���� �ٶ��ϴ�.
    )
) 

endlocal
