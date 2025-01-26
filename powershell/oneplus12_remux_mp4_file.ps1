# Get the file path from input
param (
    [string]$filePath
)

# Validate the input file
if (-Not (Test-Path $filePath)) {
    Write-Host "The specified file does not exist: $filePath" -ForegroundColor Red
    exit
}

# Validate the file extension
if ($filePath -notlike "*.mp4") {
    Write-Host "The specified file is not an MP4 file: $filePath" -ForegroundColor Red
    exit
}

Write-Host "Processing file: $filePath" -ForegroundColor Cyan

$directory = Split-Path -Parent $filePath
$baseName = [System.IO.Path]::GetFileNameWithoutExtension($filePath)

# Remux the MP4 file to MKV
$outputFileMkv = "$directory\$baseName.mkv"
Write-Host "Remuxing $filePath to $outputFileMkv"
ffmpeg -y -i "$filePath" -c copy -map_metadata 0 "$outputFileMkv"

# Check if remuxing was successful
if (Test-Path $outputFileMkv) {
    Write-Host "Successfully remuxed: $filePath -> $outputFileMkv" -ForegroundColor Green
} else {
    Write-Host "Failed to remux: $filePath" -ForegroundColor Red
    exit
}

# Convert the MKV file back to MP4
$outputFileMp4 = "$directory\$baseName.mp4"
Write-Host "Converting $outputFileMkv back to $outputFileMp4"
ffmpeg -y -i "$outputFileMkv" -c copy -map_metadata 0 "$outputFileMp4"

# Check if the conversion was successful
if (Test-Path $outputFileMp4) {
    Write-Host "Successfully converted: $outputFileMkv -> $outputFileMp4" -ForegroundColor Green

    # Overwrite the original MKV file by replacing it with the new one
    Remove-Item -Force "$outputFileMkv"
    Write-Host "Deleted original MKV: $outputFileMkv" -ForegroundColor Yellow
} else {
    Write-Host "Failed to convert: $outputFileMkv" -ForegroundColor Red
}
