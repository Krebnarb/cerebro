# Get the current directory
$directory = Get-Location

# Loop through all MP4 files in the directory
Get-ChildItem -Path $directory -Filter "*.mp4" | ForEach-Object {
    $inputFile = $_.FullName  # Full path of the input file
    $outputFile = "$($directory)\$($_.BaseName).mkv"  # Output file with .mkv extension

    # Call FFmpeg to remux the file
    Write-Host "Remuxing $inputFile to $outputFile"
    ffmpeg -i "$inputFile" -c copy "$outputFile"

    # Check if remuxing was successful
    if (Test-Path $outputFile) {
        Write-Host "Successfully remuxed: $inputFile -> $outputFile"
    } else {
        Write-Host "Failed to remux: $inputFile"
    }
}

# Get the current directory
$directory = Get-Location

# Loop through all MKV files in the directory
Get-ChildItem -Path $directory -Filter "*.mkv" | ForEach-Object {
    $inputFile = $_.FullName  # Full path of the input MKV file
    $outputFile = "$($directory)\$($_.BaseName).mp4"  # Output MP4 file path

    # Call FFmpeg to remux the MKV back to MP4
    Write-Host "Converting $inputFile back to $outputFile"
    ffmpeg -y -i "$inputFile" -c copy "$outputFile"

    # Check if the conversion was successful
    if (Test-Path $outputFile) {
        Write-Host "Successfully converted: $inputFile -> $outputFile"

        # Overwrite the original MP4 file by replacing it with the new one
        Remove-Item -Force "$inputFile"
        Write-Host "Deleted original MKV: $inputFile"
    } else {
        Write-Host "Failed to convert: $inputFile"
    }
}