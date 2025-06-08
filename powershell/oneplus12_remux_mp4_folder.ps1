# Get the directory path from input
param (
    [string]$directory = $(Get-Location)  # Default to the current directory if no input is provided
)

# Validate the input directory
if (-Not (Test-Path $directory)) {
    Write-Host "The specified directory does not exist: $directory" -ForegroundColor Red
    exit
}

Write-Host "Processing files in directory: $directory" -ForegroundColor Cyan

# Loop through all MP4 files in the directory
Get-ChildItem -Path $directory -Filter "*.mp4" | ForEach-Object {
    $filePath = $_.FullName
    $baseName = [System.IO.Path]::GetFileNameWithoutExtension($filePath)
    $outputFileMkv = "$directory\$baseName.mkv"
    $outputFileMp4 = "$directory\$baseName.mp4"

    # Remux the MP4 file to MKV
    Write-Host "Remuxing $filePath to $outputFileMkv"
    ffmpeg -y -i "$filePath" -c copy -map_metadata 0 "$outputFileMkv"

    # Check if remuxing was successful
    if (Test-Path $outputFileMkv) {
        Write-Host "Successfully remuxed: $filePath -> $outputFileMkv" -ForegroundColor Green
    } else {
        Write-Host "Failed to remux: $filePath" -ForegroundColor Red
        return
    }

    # Convert the MKV file back to MP4
    Write-Host "Converting $outputFileMkv back to $outputFileMp4"
    ffmpeg -y -i "$outputFileMkv" -c copy -map_metadata 0 "$outputFileMp4"

    # Check if the conversion was successful
    if (Test-Path $outputFileMp4) {
        Write-Host "Successfully converted: $outputFileMkv -> $outputFileMp4" -ForegroundColor Green
        Remove-Item -Force "$outputFileMkv"
        Write-Host "Deleted original MKV: $outputFileMkv" -ForegroundColor Yellow
    } else {
        Write-Host "Failed to convert: $outputFileMkv" -ForegroundColor Red
    }
}
