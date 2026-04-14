[CmdletBinding()]
param(
    [string]$SourceDir = "",
    [string]$CodexHome = "",
    [switch]$Force
)

$ErrorActionPreference = "Stop"

function Resolve-FullPath {
    param([Parameter(Mandatory = $true)][string]$PathValue)
    return [System.IO.Path]::GetFullPath($PathValue)
}

function Copy-SkillPayload {
    param(
        [Parameter(Mandatory = $true)][string]$SourcePath,
        [Parameter(Mandatory = $true)][string]$TargetPath
    )

    New-Item -ItemType Directory -Path $TargetPath -Force | Out-Null
    foreach ($name in @("SKILL.md", "agents", "assets", "references", "scripts")) {
        $sourceItem = Join-Path $SourcePath $name
        if (-not (Test-Path -LiteralPath $sourceItem)) {
            continue
        }
        $targetItem = Join-Path $TargetPath $name
        if (Test-Path -LiteralPath $targetItem) {
            Remove-Item -LiteralPath $targetItem -Recurse -Force
        }
        Copy-Item -LiteralPath $sourceItem -Destination $targetItem -Recurse -Force
    }
}

function Remove-PycacheDirs {
    param([Parameter(Mandatory = $true)][string]$RootPath)
    if (-not (Test-Path -LiteralPath $RootPath)) {
        return
    }

    Get-ChildItem -LiteralPath $RootPath -Recurse -Directory -Force |
        Where-Object { $_.Name -eq "__pycache__" } |
        ForEach-Object {
            Remove-Item -LiteralPath $_.FullName -Recurse -Force
        }
}

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$repoRoot = Resolve-FullPath (Join-Path $scriptDir "..")

if (-not $SourceDir) {
    $SourceDir = $repoRoot
}
if (-not $CodexHome) {
    $CodexHome = Join-Path $HOME ".codex"
}

$sourceDirFull = Resolve-FullPath $SourceDir
$codexHomeFull = Resolve-FullPath $CodexHome
$skillsRoot = Join-Path $codexHomeFull "skills"
$targetDir = Join-Path $skillsRoot "learning-coach"

if (-not (Test-Path -LiteralPath $sourceDirFull)) {
    throw "找不到 skill 源目录：$sourceDirFull"
}

New-Item -ItemType Directory -Path $skillsRoot -Force | Out-Null

if (Test-Path -LiteralPath $targetDir) {
    if (-not $Force) {
        Write-Host "目标目录已存在：$targetDir"
        Write-Host "如需覆盖，请重新执行并加上 -Force。"
        exit 1
    }
    Remove-Item -LiteralPath $targetDir -Recurse -Force
}

Copy-SkillPayload -SourcePath $sourceDirFull -TargetPath $targetDir
Remove-PycacheDirs -RootPath $targetDir

Write-Host ""
Write-Host "安装完成。"
Write-Host "skill 目录：$targetDir"
Write-Host ""
Write-Host "推荐下一步："
Write-Host '1. 在 Codex 里直接说：使用 $learning-coach 帮我开始一个新的学习项目'
Write-Host "2. 或手动运行：python `"$targetDir\scripts\learn.py`""
