@echo off
setlocal

rem ���� ��� ����
set file_path=C:\Program Files (x86)\evEraser_Win\evEraser.exe

rem ���� ���� ���� Ȯ��
if exist "%file_path%" (
    echo ��ȣ
    echo ���� ����: evEraser ��ġ�Ǿ� �ֽ��ϴ�. 
) else (
    echo ����
    echo ���� ����: evEraser �̼�ġ�Ǿ� �ֽ��ϴ�. 
    echo ��ġ ���: SKT AD ��ġ �� ������ ���ӵǾ� ������ �ڵ� ��ġ�ǳ� ������ �ִ� ��� Help Desk ���� �ٶ��ϴ�.
)

endlocal
rem pause