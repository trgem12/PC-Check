@echo off
setlocal

REM ���� ������ ���Ϸ� ��������
secedit /export /cfg tempcfg.ini >nul 2>&1

REM '���� �ܼ� �ڵ� �α׿� ���' ���� Ȯ��
type tempcfg.ini | findstr /C:"RecoveryConsole: Allow automatic administrative logon" >nul
if %errorlevel%==0 (
    echo ����
    echo �������: ���� �ܼ� �ڵ� �α׿� ����� Ȱ��ȭ�Ǿ� �ֽ��ϴ�.
    echo ��ġ���: �����ǡ������������ú�����å�溸�ȼ����������å�溸�ȿɼǡ溹���ܼ�:�ڵ������α׿����Ӽ�'��� �� ��'���� ����
) else (
    echo ��ȣ
    echo �������: '���� �ܼ� �ڵ� �α׿� ���'�� ��Ȱ��ȭ�Ǿ� �ֽ��ϴ�.
)

REM �ӽ� ���� ����
del tempcfg.ini >nul

endlocal

