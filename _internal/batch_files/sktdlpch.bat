@echo off
setlocal

rem ���� ���� Ȯ��
for /f "tokens=3" %%a in ('sc query edpa ^| findstr "����"') do (
    set service_status=%%a
)

rem ����� ���� ���� �� ���
rem echo ����� ���� ���� ��: %service_status%

rem ���� ���¿� ���� �޽��� ���
if "%service_status%"=="4" (
    echo ��ȣ
    echo �������: DLP ��ġ�Ǿ� �ֽ��ϴ�.
) else (
    echo ����
    echo �������: DLP �̼�ġ�Ǿ� �ֽ��ϴ�. 
    echo ��ġ���: 
    echo 1. �系�� 150�� ����
    echo 2. cmd �� sc start edpa �Է��Ͽ� ���� ���� ����
    echo 3. cmd �� sc query edpa �Է� �� ���� ���� �� RUNNING Ȯ��
    echo 4. �۾������� �� �������� �� edpa.exe ��Ŭ�� �� �Ӽ� �� �ڼ��� �� 15.8.300 ���� Ȯ��
    echo 5. �� �������� ��ġ�� �ȵǴ� ��� SKT IT���ȿ�� �����´� �Ǵ� �ǿ����Բ� ����
)

endlocal

