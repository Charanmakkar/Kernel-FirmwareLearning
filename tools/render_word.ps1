$ErrorActionPreference = 'Stop'
$workspacePath = Split-Path -Parent $PSScriptRoot
$editionPath = Join-Path $workspacePath 'Embedded_Linux_Kernel_Firmware_Learning\Word_Edition'
$previewPath = Join-Path $workspacePath 'release_previews'
New-Item -ItemType Directory -Path $previewPath -Force | Out-Null
$wordApp = $null
$results = @()
try {
    $wordApp = New-Object -ComObject Word.Application
    $wordApp.Visible = $false
    $wordApp.DisplayAlerts = 0
    foreach ($wordFile in Get-ChildItem -LiteralPath $editionPath -Filter '*.docx') {
        $document = $null
        try {
            $document = $wordApp.Documents.Open($wordFile.FullName, $false, $false, $false)
            $document.Fields.Update() | Out-Null
            foreach ($contents in $document.TablesOfContents) { $contents.Update() }
            $document.Repaginate()
            $document.Save()
            $pdfPath = Join-Path $previewPath ($wordFile.BaseName + '.pdf')
            $document.ExportAsFixedFormat($pdfPath, 17)
            $results += [PSCustomObject]@{file=$wordFile.Name; pages=$document.ComputeStatistics(2); pdf=$pdfPath; result='rendered with Microsoft Word'}
        }
        finally {
            if ($null -ne $document) { $document.Close(0); [void][Runtime.InteropServices.Marshal]::ReleaseComObject($document) }
        }
    }
    $results | ConvertTo-Json -Depth 4 | Set-Content -LiteralPath (Join-Path $previewPath 'render_status.json') -Encoding UTF8
    $results | Select-Object file,pages,result | Format-Table -AutoSize
}
finally {
    if ($null -ne $wordApp) { $wordApp.Quit(0); [void][Runtime.InteropServices.Marshal]::ReleaseComObject($wordApp) }
}
