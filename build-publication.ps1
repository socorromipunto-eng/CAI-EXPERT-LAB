$ErrorActionPreference = "Stop"

$Root = $PSScriptRoot
$OutputDirectory = Join-Path $Root "output"
$MergedMarkdown = Join-Path $OutputDirectory "CAI-EXPERT-LAB.md"
$WordDocument = Join-Path $OutputDirectory "CAI-EXPERT-LAB-Copyright-Edition.docx"

$Folders = @(
    "CAI-Engine",
    "docs",
    "labs",
    "legal"
)

if (Test-Path $OutputDirectory) {
    Remove-Item $OutputDirectory -Recurse -Force
}

New-Item -ItemType Directory -Path $OutputDirectory -Force | Out-Null

$Document = [System.Text.StringBuilder]::new()

[void]$Document.AppendLine("---")
[void]$Document.AppendLine('title: "CAI EXPERT LAB"')
[void]$Document.AppendLine('author: "Antonio José Socorro Marín"')
[void]$Document.AppendLine('subtitle: "Copyright Deposit Edition"')
[void]$Document.AppendLine('lang: en-US')
[void]$Document.AppendLine('toc: true')
[void]$Document.AppendLine('toc-depth: 3')
[void]$Document.AppendLine('numbersections: true')
[void]$Document.AppendLine("---")
[void]$Document.AppendLine("")

function Get-Title {
    param([string]$Text)

    $Title = [System.IO.Path]::GetFileNameWithoutExtension($Text)
    $Title = $Title -replace "[-_]+", " "
    $Title = $Title -replace "\s+", " "

    return $Title.Trim()
}

function Add-MarkdownFile {
    param([System.IO.FileInfo]$File)

    $RelativePath = [System.IO.Path]::GetRelativePath(
        $Root,
        $File.FullName
    )

    if ($File.Name -ieq "README.md") {
        $Title = Get-Title (Split-Path $File.DirectoryName -Leaf)
    }
    else {
        $Title = Get-Title $File.Name
    }

    Write-Host "Adding: $RelativePath"

    [void]$Document.AppendLine("")
    [void]$Document.AppendLine("\newpage")
    [void]$Document.AppendLine("")
    [void]$Document.AppendLine("## $Title")
    [void]$Document.AppendLine("")
    [void]$Document.AppendLine("*Source: $RelativePath*")
    [void]$Document.AppendLine("")

    $Content = Get-Content `
        -LiteralPath $File.FullName `
        -Raw `
        -Encoding UTF8

    $Content = $Content -replace "(?m)^######\s+", "######## "
    $Content = $Content -replace "(?m)^#####\s+", "####### "
    $Content = $Content -replace "(?m)^####\s+", "###### "
    $Content = $Content -replace "(?m)^###\s+", "##### "
    $Content = $Content -replace "(?m)^##\s+", "#### "
    $Content = $Content -replace "(?m)^#\s+", "### "

    [void]$Document.AppendLine($Content.Trim())
    [void]$Document.AppendLine("")
}

foreach ($Folder in $Folders) {
    $FolderPath = Join-Path $Root $Folder

    if (-not (Test-Path $FolderPath)) {
        Write-Warning "Folder not found: $Folder"
        continue
    }

    [void]$Document.AppendLine("")
    [void]$Document.AppendLine("\newpage")
    [void]$Document.AppendLine("")
    [void]$Document.AppendLine("# $(Get-Title $Folder)")
    [void]$Document.AppendLine("")

    $Files = Get-ChildItem `
        -Path $FolderPath `
        -Filter "*.md" `
        -File `
        -Recurse |
        Where-Object {
            $_.FullName -notmatch "[\\/](output|\.git)[\\/]"
        } |
        Sort-Object `
            @{ Expression = { if ($_.Name -ieq "README.md") { 0 } else { 1 } } },
            @{ Expression = { $_.FullName } }

    foreach ($File in $Files) {
        Add-MarkdownFile -File $File
    }
}

$LicensePath = Join-Path $Root "LICENSE.md"

if (Test-Path $LicensePath) {
    [void]$Document.AppendLine("")
    [void]$Document.AppendLine("\newpage")
    [void]$Document.AppendLine("")
    [void]$Document.AppendLine("# License and Copyright Notice")
    [void]$Document.AppendLine("")

    $LicenseContent = Get-Content `
        -LiteralPath $LicensePath `
        -Raw `
        -Encoding UTF8

    $LicenseContent = $LicenseContent -replace "(?m)^#\s+", "## "

    [void]$Document.AppendLine($LicenseContent.Trim())
}

[System.IO.File]::WriteAllText(
    $MergedMarkdown,
    $Document.ToString(),
    [System.Text.UTF8Encoding]::new($false)
)

& pandoc `
    $MergedMarkdown `
    --from=markdown `
    --to=docx `
    --standalone `
    --toc `
    --toc-depth=3 `
    --number-sections `
    --resource-path="$Root" `
    --output="$WordDocument"

if ($LASTEXITCODE -ne 0) {
    throw "Pandoc failed with exit code $LASTEXITCODE"
}

if (-not (Test-Path $WordDocument)) {
    throw "The Word document was not created."
}

Write-Host ""
Write-Host "Document created successfully:"
Write-Host $WordDocument