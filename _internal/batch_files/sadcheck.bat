@echo off
setlocal

rem ������ �̸��� Ȯ���� ���
set target_domain=SKT.AD

rem ���� PC�� ������ ��������
for /f "tokens=*" %%a in ('echo %USERDNSDOMAIN%') do set current_domain=%%a

rem ������ �̸� ��
if /i "%current_domain%"=="%target_domain%" (
    echo ��ȣ
    echo ���� ����: %current_domain% �����ο� ����Ǿ� �ֽ��ϴ�.
) else (
    echo ����
    echo �������: SKT AD ������Ǿ� �ֽ��ϴ�. 
    echo ��ġ���: Help Desk ��ǻ�� ������ �缳ġ �� �ʱ⼳�� ��� �ȳ� �� �����Ͽ� SKT AD ��ġ
)

endlocal
