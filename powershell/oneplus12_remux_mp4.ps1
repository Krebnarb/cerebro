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
    $inputFile = $_.FullName  # Full path of the input file
    $outputFile = "$($directory)\$($_.BaseName).mkv"  # Output file with .mkv extension

    # Call FFmpeg to remux the file
    Write-Host "Remuxing $inputFile to $outputFile"
    ffmpeg -y -i "$inputFile" -c copy -map_metadata 0 "$outputFile"

    # Check if remuxing was successful
    if (Test-Path $outputFile) {
        Write-Host "Successfully remuxed: $inputFile -> $outputFile" -ForegroundColor Green
    } else {
        Write-Host "Failed to remux: $inputFile" -ForegroundColor Red
    }
}

# Loop through all MKV files in the directory
Get-ChildItem -Path $directory -Filter "*.mkv" | ForEach-Object {
    $inputFile = $_.FullName  # Full path of the input MKV file
    $outputFile = "$($directory)\$($_.BaseName).mp4"  # Output MP4 file path

    # Call FFmpeg to remux the MKV back to MP4
    Write-Host "Converting $inputFile back to $outputFile"
    ffmpeg -y -i "$inputFile" -c copy -map_metadata 0 "$outputFile"

    # Check if the conversion was successful
    if (Test-Path $outputFile) {
        Write-Host "Successfully converted: $inputFile -> $outputFile" -ForegroundColor Green

        # Overwrite the original MKV file by replacing it with the new one
        Remove-Item -Force "$inputFile"
        Write-Host "Deleted original MKV: $inputFile" -ForegroundColor Yellow
    } else {
        Write-Host "Failed to convert: $inputFile" -ForegroundColor Red
    }
}
