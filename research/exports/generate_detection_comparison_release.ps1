# Release-safe comparison figure. This script does not invoke a model or experiment runner.
# Values are the audited Full Rules/IF/LSTM/Combined metrics in FINAL_RAW_CSV_RECALCULATION.txt.
param(
    [string]$OutputPath = "C:\DL_PROJECT\research\exports\detection_comparison_release.png"
)

Set-StrictMode -Version Latest
Add-Type -AssemblyName System.Drawing

$dir = Split-Path -Parent $OutputPath
if (-not (Test-Path -LiteralPath $dir)) { New-Item -ItemType Directory -Path $dir -Force | Out-Null }

$width = 1800; $height = 1120
$bitmap = [System.Drawing.Bitmap]::new($width, $height)
$graphics = [System.Drawing.Graphics]::FromImage($bitmap)
$graphics.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
$graphics.TextRenderingHint = [System.Drawing.Text.TextRenderingHint]::ClearTypeGridFit
$graphics.Clear([System.Drawing.Color]::White)

$navy = [System.Drawing.Color]::FromArgb(30, 41, 59)
$slate = [System.Drawing.Color]::FromArgb(71, 85, 105)
$grid = [System.Drawing.Color]::FromArgb(226, 232, 240)
$blue = [System.Drawing.Color]::FromArgb(37, 99, 235)
$green = [System.Drawing.Color]::FromArgb(16, 185, 129)
$orange = [System.Drawing.Color]::FromArgb(234, 88, 12)
$noteBg = [System.Drawing.Color]::FromArgb(240, 249, 255)
$noteBorder = [System.Drawing.Color]::FromArgb(125, 211, 252)

$title = [System.Drawing.Font]::new('Arial', 28, [System.Drawing.FontStyle]::Bold)
$subtitle = [System.Drawing.Font]::new('Arial', 16, [System.Drawing.FontStyle]::Regular)
$label = [System.Drawing.Font]::new('Arial', 15, [System.Drawing.FontStyle]::Regular)
$group = [System.Drawing.Font]::new('Arial', 16, [System.Drawing.FontStyle]::Bold)
$value = [System.Drawing.Font]::new('Arial', 14, [System.Drawing.FontStyle]::Bold)
$note = [System.Drawing.Font]::new('Arial', 15, [System.Drawing.FontStyle]::Regular)

function DrawText([string]$Text, [System.Drawing.Font]$Font, [System.Drawing.Color]$Color, [float]$X, [float]$Y) {
    $brush = [System.Drawing.SolidBrush]::new($Color)
    $graphics.DrawString($Text, $Font, $brush, $X, $Y)
    $brush.Dispose()
}
function DrawCentered([string]$Text, [System.Drawing.Font]$Font, [System.Drawing.Color]$Color, [float]$CenterX, [float]$Y) {
    $size = $graphics.MeasureString($Text, $Font)
    DrawText $Text $Font $Color ([float]($CenterX - ($size.Width / 2))) $Y
}

DrawText 'Figure A.2 (Release Candidate): Audited Detection Comparison' $title $navy 64 40
DrawText 'Synthetic batch benchmark: N=320 windows (200 normal, 120 fault across six archetypes)' $subtitle $slate 64 86
DrawText 'Source: FINAL_RAW_CSV_RECALCULATION.txt. Only Full Rules, Isolation Forest, LSTM AE, and Combined Alert are plotted.' $subtitle $slate 64 112

# Legend
$legend = @(@('Precision', $blue), @('Recall', $green), @('F1 score', $orange))
$legendX = 1090
foreach ($item in $legend) {
    $brush = [System.Drawing.SolidBrush]::new($item[1])
    $graphics.FillRectangle($brush, $legendX, 74, 22, 22)
    $brush.Dispose()
    DrawText $item[0] $label $slate ($legendX + 30) 74
    $legendX += 155
}

# Metrics chart
$left = 110; $top = 205; $chartWidth = 1540; $chartHeight = 470; $bottom = $top + $chartHeight
$penAxis = [System.Drawing.Pen]::new($slate, 2)
$penGrid = [System.Drawing.Pen]::new($grid, 1)
$graphics.DrawLine($penAxis, $left, $top, $left, $bottom)
$graphics.DrawLine($penAxis, $left, $bottom, ($left + $chartWidth), $bottom)
foreach ($tick in @(0.0, 0.2, 0.4, 0.6, 0.8, 1.0)) {
    $y = $bottom - ($tick * $chartHeight)
    $graphics.DrawLine($penGrid, $left, $y, ($left + $chartWidth), $y)
    DrawText ($tick.ToString('0.0')) $label $slate 58 ($y - 10)
}
DrawText 'Score' $group $navy 62 180

$models = @(
    [PSCustomObject]@{ Name = 'Full Operational Rules'; Precision = 1.0000; Recall = 1.0000; F1 = 1.0000; Latency = '0.01 ms' },
    [PSCustomObject]@{ Name = 'Isolation Forest'; Precision = 0.9344; Recall = 0.4750; F1 = 0.6298; Latency = '1.84 ms' },
    [PSCustomObject]@{ Name = 'LSTM Autoencoder'; Precision = 0.9836; Recall = 1.0000; F1 = 0.9917; Latency = '0.17 ms' },
    [PSCustomObject]@{ Name = 'Combined Alert'; Precision = 0.9836; Recall = 1.0000; F1 = 0.9917; Latency = '0.18 ms' }
)
$groupWidth = $chartWidth / $models.Count
$barWidth = 58
for ($i = 0; $i -lt $models.Count; $i++) {
    $model = $models[$i]
    $center = $left + ($groupWidth * $i) + ($groupWidth / 2)
    $bars = @(@($model.Precision, $blue), @($model.Recall, $green), @($model.F1, $orange))
    for ($j = 0; $j -lt $bars.Count; $j++) {
        $barX = $center - 100 + ($j * 70)
        $barH = $bars[$j][0] * $chartHeight
        $barY = $bottom - $barH
        $brush = [System.Drawing.SolidBrush]::new($bars[$j][1])
        $graphics.FillRectangle($brush, [int]$barX, [int]$barY, $barWidth, [int]$barH)
        $brush.Dispose()
        DrawCentered ($bars[$j][0].ToString('0.0000')) $value $navy ($barX + ($barWidth / 2)) ($barY - 28)
    }
    DrawCentered $model.Name $group $navy $center ($bottom + 18)
}

# Measured latency table - no operational FA/hr calculation is displayed.
$tableTop = 790; $tableLeft = 110; $tableWidth = 1540; $rowHeight = 58
$tableBrush = [System.Drawing.SolidBrush]::new($noteBg)
$graphics.FillRectangle($tableBrush, $tableLeft, $tableTop, $tableWidth, ($rowHeight * 2))
$tableBrush.Dispose()
$tablePen = [System.Drawing.Pen]::new($noteBorder, 2)
$graphics.DrawRectangle($tablePen, $tableLeft, $tableTop, $tableWidth, ($rowHeight * 2))
$columnXs = @(($tableLeft + 420), ($tableLeft + 720), ($tableLeft + 1020), ($tableLeft + 1280))
foreach ($x in $columnXs) { $graphics.DrawLine($tablePen, $x, $tableTop, $x, ($tableTop + ($rowHeight * 2))) }
$graphics.DrawLine($tablePen, $tableLeft, ($tableTop + $rowHeight), ($tableLeft + $tableWidth), ($tableTop + $rowHeight))
$graphics.DrawLine($tablePen, $tableLeft, ($tableTop + ($rowHeight * 2)), ($tableLeft + $tableWidth), ($tableTop + ($rowHeight * 2)))
DrawText 'Measured mean latency' $group $navy ($tableLeft + 18) ($tableTop + 15)
DrawText 'Full Rules' $group $navy ($tableLeft + 440) ($tableTop + 15)
DrawText 'Isolation Forest' $group $navy ($tableLeft + 740) ($tableTop + 15)
DrawText 'LSTM AE' $group $navy ($tableLeft + 1040) ($tableTop + 15)
DrawText 'Combined' $group $navy ($tableLeft + 1300) ($tableTop + 15)
DrawText 'Latency' $label $slate ($tableLeft + 18) ($tableTop + 75)
DrawText '0.01 ms' $value $navy ($tableLeft + 440) ($tableTop + 75)
DrawText '1.84 ms' $value $navy ($tableLeft + 740) ($tableTop + 75)
DrawText '0.17 ms' $value $navy ($tableLeft + 1040) ($tableTop + 75)
DrawText '0.18 ms' $value $navy ($tableLeft + 1300) ($tableTop + 75)

DrawText 'Operational false alarms per hour: UNAVAILABLE. This non-streaming batch evaluation does not measure continuous alert rate or deduplication.' $note $navy 112 1000

$bitmap.Save($OutputPath, [System.Drawing.Imaging.ImageFormat]::Png)
$tablePen.Dispose(); $penAxis.Dispose(); $penGrid.Dispose()
$title.Dispose(); $subtitle.Dispose(); $label.Dispose(); $group.Dispose(); $value.Dispose(); $note.Dispose()
$graphics.Dispose(); $bitmap.Dispose()
Write-Output "Created release-safe figure: $OutputPath"
