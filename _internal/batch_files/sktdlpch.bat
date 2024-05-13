@echo off
setlocal

rem 서비스 상태 확인
for /f "tokens=3" %%a in ('sc query edpa ^| findstr "상태"') do (
    set service_status=%%a
)

rem 추출된 서비스 상태 값 출력
rem echo 추출된 서비스 상태 값: %service_status%

rem 서비스 상태에 따른 메시지 출력
if "%service_status%"=="4" (
    echo 양호
    echo 현재상태: DLP 설치되어 있습니다.
) else (
    echo 미흡
    echo 현재상태: DLP 미설치되어 있습니다. 
    echo 조치방법: 
    echo 1. 사내망 150망 접속
    echo 2. cmd → sc start edpa 입력하여 서비스 구동 시작
    echo 3. cmd → sc query edpa 입력 후 서비스 상태 값 RUNNING 확인
    echo 4. 작업관리자 → 세부정보 → edpa.exe 우클릭 → 속성 → 자세히 → 15.8.300 버전 확인
    echo 5. 위 과정으로 조치가 안되는 경우 SKT IT보안운영팀 박준태님 또는 권오성님께 문의
)

endlocal

