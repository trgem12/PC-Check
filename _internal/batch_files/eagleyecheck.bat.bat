@echo off
setlocal

rem Ȯ���� ���α׷��� ��ġ ���
set program_path="C:\iEC\iECUI.exe"

rem ���α׷� ������ �����ϴ��� Ȯ��
if exist %program_path% (
    echo ��ȣ
    echo ���� ����: �̱۾��� ��ġ�Ǿ� �ֽ��ϴ�.
) else (
    echo ����
    echo ���� ����: �̱۾��� �̼�ġ�Ǿ� �ֽ��ϴ�. 
    echo ��ġ ���: i-net��sk ons store��PC Tab���̱۾��� �ٿ�ε� �� ��ġ 
)

endlocal
rem pause
