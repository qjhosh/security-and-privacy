# 生成当前时间戳（ISO格式）
$timestamp = Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ"

# 运行 netstat 并筛选 TCP 连接
$netstat = netstat -n | Select-String "TCP"
$summary = @{}

# 解析每一行的远程 IP 地址（IPv4 / IPv6）
foreach ($line in $netstat) {
    if ($line -match "\s+\S+\s+(\[?[0-9a-fA-F\.:]+\]?):\d+") {
        $ip = $matches[1] -replace "^\[|\]$"  # 去掉 IPv6 的 [ 和 ]
        if ($ip -and $ip -ne "0.0.0.0" -and $ip -ne "127.0.0.1" -and $ip -ne "::1") {
            if ($summary.ContainsKey($ip)) {
                $summary[$ip] += 1
            } else {
                $summary[$ip] = 1
            }
        }
    }
}

# 指定输出日志路径
$logpath = "D:\homework\ucl\sap\try2\logdata\netstat.log"

# 写入时间戳标题
"=== Netstat Snapshot at $timestamp ===" | Out-File -FilePath $logpath -Encoding UTF8 -Append

# ✅ 显式逐条写入 IP 和连接数，避免数组格式或换行错误
foreach ($ip in $summary.Keys) {
    "$($summary[$ip]) $ip" | Out-File -FilePath $logpath -Encoding UTF8 -Append
}
