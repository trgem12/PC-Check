@echo off

set SCRNSAVE_KEY="HKEY_CURRENT_USER\Control Panel\Desktop"
set SCRNSAVE_VALUE="SCRNSAVE.EXE"

for /f "tokens=2* delims= " %%a in ('reg query %SCRNSAVE_KEY% /v %SCRNSAVE_VALUE%') do (
    set SCRNSAVE_PATH=%%b
)

if not defined SCRNSAVE_PATH (
    echo ��ȣ
    echo ���� ����: ȭ�麸ȣ�Ⱑ �����Ǿ� �ֽ��ϴ�.
) else (
    echo ����
    echo ���� ����: ȭ�麸ȣ�Ⱑ �����Ǿ� ���� �ʽ��ϴ�. 
    echo ��ġ ���: SKT AD�� ���� ����Ǵ� �κ����� AD �缳ġ�� �ʿ��մϴ�. 
)