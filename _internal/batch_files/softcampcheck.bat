@echo off
setlocal

rem Ȯ���� ���α׷� ���� ���
set program_path="C:\Windows\Softcamp\SDS\SDSHlpr.exe"

rem ���α׷� ������ �����ϴ��� Ȯ��
if exist "%program_path%" (
    echo ��ȣ
    echo �������: �������� ��ġ�Ǿ� �ֽ��ϴ�. 
) else (
    echo ����
    echo �������: �������� �̼�ġ�Ǿ� �ֽ��ϴ�. 
    echo ��ġ���: i-net��sk ons store�湮������ �ٿ�ε� �� ��ġ 
)

endlocal
rem pause