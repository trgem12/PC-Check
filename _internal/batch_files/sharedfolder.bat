@echo off
setlocal enabledelayedexpansion

:: Script to check shared folders on a Windows 10 PC

:: Variable to store non-conforming shared folder names
set "nonConformingShares="

:: Iterate through the list of shared folders, filtering out irrelevant lines
for /f "tokens=1" %%i in ('net share ^| findstr /R /C:"^[A-Z].*[ ]*$"') do (
    set "share=%%i"
    :: Check if the share does not end with '$'
    if not "!share:~-1!"=="$" (
        set "nonConformingShares=!nonConformingShares! %%i"
    )
)

:: Check if any non-conforming shares were found and output the result
if "!nonConformingShares!"=="" (
    echo 양호
    echo 현재 상태: 공유 폴더는 없습니다.
) else (
    echo 미흡
    echo 현재 상태: 공유 폴더가 설정되어 있습니다. !nonConformingShares!
    echo 조치 방법: 
    echo 1. 공유폴더 확인 시작 → 실행 → fsmgmt.msc 입력
    echo 2. 불필요한 공유 폴더 확인 → 해당 공유 폴더 우클릭 → 공유 중지
    echo 3. cmd → net share [삭제할 공유 폴더명] /delete로 삭제 처리
)


endlocal
