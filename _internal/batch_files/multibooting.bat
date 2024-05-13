@echo off
setlocal enabledelayedexpansion

REM bcdedit 명령어를 실행하여 부트 엔트리의 'description' 값을 가져옵니다.
set "count=0"
for /f "tokens=1* delims=: " %%a in ('bcdedit /enum ^| findstr /c:"Windows 10" /c:"description"') do (
    if "%%a"=="description" (
        if not "%%b"=="Windows Boot Manager" (
            set /a count+=1
            set "os[!count!]=%%b"
        )
    )
)

REM 부트 엔트리의 수를 확인하여 결과를 출력합니다.
if !count! equ 1 (
    echo 양호
    echo 현재 상태: 현재 PC에 !os[1]! 만 설치되어 있습니다.
) else if !count! gtr 1 (
    echo 미흡
    for /l %%i in (1, 1, !count!) do (
        echo 현재 상태: PC에 2개 이상의 OS %%i: !os[%%i]! 가 설치되어 있습니다.
        echo 조치 방법: 시작→실행→msconfig 입력→시스템구성 부팅 탭→사용하지 않는 OS 삭제 바랍니다.
    )
) 

endlocal
