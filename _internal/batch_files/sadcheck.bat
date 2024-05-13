@echo off
setlocal

rem 도메인 이름을 확인할 대상
set target_domain=SKT.AD

rem 현재 PC의 도메인 가져오기
for /f "tokens=*" %%a in ('echo %USERDNSDOMAIN%') do set current_domain=%%a

rem 도메인 이름 비교
if /i "%current_domain%"=="%target_domain%" (
    echo 양호
    echo 현재 상태: %current_domain% 도메인에 연결되어 있습니다.
) else (
    echo 미흡
    echo 현재상태: SKT AD 미적용되어 있습니다. 
    echo 조치방법: Help Desk 컴퓨터 윈도우 재설치 후 초기설정 방법 안내 글 참고하여 SKT AD 설치
)

endlocal
