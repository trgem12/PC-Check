@echo off
powershell -Command "$shell = New-Object -ComObject Shell.Application; $recBin = $shell.Namespace(0xA); $count = $recBin.Items().Count; if ($count -gt 0) { Write-Host '����'; Write-Host \"���� ����: �����뿡 ������ $count �� �ֽ��ϴ�.\"; Write-Host '��ġ ���: ������ ��Ŭ�� �� ������ ���� Ŭ��'; } else { Write-Host '��ȣ'; Write-Host \"���� ����: �����뿡 ������ �����ϴ�.\"; }"
