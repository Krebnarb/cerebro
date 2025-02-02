param (
    [string]$inputDir
)

# Check if input directory is provided
if (-not $inputDir) {
    Write-Host "Usage: .\create_proxies.ps1 -inputDir 'C:\path\to\videos'"
    exit 1
}

# Resolve full path
$inputDir = Resolve-Path $inputDir
$outputDir = Join-Path $inputDir "proxy_videos"

# Set encoding parameters
$bitrate = "4M"
$resolution = "1920x1080"

# Ensure output directory exists
if (!(Test-Path -Path $outputDir)) {
    New-Item -ItemType Directory -Path $outputDir | Out-Null
}

# Get all video files in the input directory
$videos = Get-ChildItem -Path $inputDir -File | Where-Object { $_.Extension -match "(\.mp4|\.MP4|\.mov|\.avi|\.mkv)$" }

Write-Output "Found $($videos.Count) video files in $inputDir"

foreach ($video in $videos) {
    # Extract filename without extension
    $filename = [System.IO.Path]::GetFileNameWithoutExtension($video.Name)
    $outputFile = Join-Path $outputDir "$filename`_proxy.mp4"

    # Construct ffmpeg command
    $ffmpegCmd = "ffmpeg -i `"$($video.FullName)`" -c:v libx264 -preset medium -b:v $bitrate -vf `"scale=$resolution`" -c:a aac -b:a 128k -movflags +faststart `"$outputFile`""

    Write-Output "Processing: $($video.Name)"

    # Run ffmpeg command
    Invoke-Expression $ffmpegCmd

    Write-Output "Proxy created: $outputFile"
}

Write-Output "All proxies have been generated."
