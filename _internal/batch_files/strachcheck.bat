@echo off
powershell -Command "$shell = New-Object -ComObject Shell.Application; $recBin = $shell.Namespace(0xA); $count = $recBin.Items().Count; if ($count -gt 0) { Write-Host '미흡'; Write-Host \"현재 상태: 휴지통에 파일이 $count 개 있습니다.\"; Write-Host '조치 방법: 휴지통 우클릭 → 휴지통 비우기 클릭'; } else { Write-Host '양호'; Write-Host \"현재 상태: 휴지통에 파일이 없습니다.\"; }"
