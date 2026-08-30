param()

$ErrorActionPreference = 'Stop'
$pluginRoot = Split-Path -Parent $PSScriptRoot
$serverPath = Join-Path $PSScriptRoot 'pixiv_mcp.py'
$configPath = Join-Path $pluginRoot '.mcp.json'

$payload = @{
    mcpServers = @{
        'pixiv-browser' = @{
            command = 'python'
            args = @($serverPath)
        }
    }
}

$payload | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath $configPath -Encoding utf8
Write-Output "Configured MCP server: $serverPath"
