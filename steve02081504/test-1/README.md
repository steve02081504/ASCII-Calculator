这是我的计划B🤠
先不用

<!--据群友说NFC橙汁不是太好喝-->

不能直接跑，需要编译

## 编译到exe

```powershell
if (!(Get-Command ps12exe -ErrorAction Ignore)) {
	Install-Module ps12exe -Scope CurrentUser -Force
}
ps12exe -inputFile ./a.ps1
./a.exe "test"
```

分数 349
