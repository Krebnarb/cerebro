// Function to format the date as "YYYY_MM_DD"
function getFormattedDate(creationDate) {
    var year = creationDate.slice(0, 4); // "YYYY"
    var month = creationDate.slice(5, 7); // "MM"
    var day = creationDate.slice(8, 10); // "DD"

    // Return formatted date as "YYYY_MM_DD"
    return year + "_" + month + "_" + day;
}

function getActiveSequence() {
    // Get the active sequence
    var activeSequence = app.project.activeSequence;

    if (activeSequence) {
        return activeSequence;
    }

    return null;
}

function getLinkedAudioFromClip(activeSequence, clip) {
    var projectItem = clip.projectItem;
    
    // Loop through all audio tracks in the sequence
    for (var i = 0; i < activeSequence.audioTracks.numTracks; i++) {
        var audioTrack = activeSequence.audioTracks[i];
        
        // Loop through the clips in the audio track
        for (var j = 0; j < audioTrack.clips.numItems; j++) {
            var audioClip = audioTrack.clips[j];
            
            // Check if the audio clip is linked to the same project item as the video clip
            if (audioClip.start.seconds === clip.start.seconds) {
                return audioClip;  // Return the corresponding audio clip
            }
        }
    }
    
    // If no corresponding audio clip is found
    return null;
}

function getBinByName(binName) {
    var targetBin = null;
    for (var i = 0; i < app.project.rootItem.children.length; i++) {
        var item = app.project.rootItem.children[i];
        if (item.name === targetBinName && item.type === ProjectItemType.BIN) {
            targetBin = item;
            break;
        }
    }

    return targetBin;
}

/**
 * Adds zero padding to an integer.
 * @param {number} num - The integer to pad.
 * @param {number} length - The desired length of the output string.
 * @returns {string} - The zero-padded string.
 */
function padWithZeros(num, length) {
    // Convert the number to a string
    var numString = String(num);
    
    // Check the current length and calculate how many zeros to add
    var zerosToAdd = length - numString.length;
    
    // If the number is already the desired length or longer, return it as is
    if (zerosToAdd <= 0) {
        return numString;
    }
    
    // Create a string of zeros and concatenate with the original number
    var paddedString = "";
    for (var i = 0; i < zerosToAdd; i++) {
        paddedString += "0";
    }
    
    return paddedString + numString; // Combine zeros with the original number
}

/**
 * Check if a bin with the specified name exists.
 * @param {string} binName - The name of the bin to check.
 * @returns {ProjectItem|null} - Returns the bin if it exists, or null if it does not.
 */
function findBinByName(binName) {
    var rootItem = app.project.rootItem;

    for (var i = 0; i < rootItem.children.length; i++) {
        var item = rootItem.children[i];
        if (item.name === binName && item.type === ProjectItemType.BIN) {
            return item; // Return the existing bin
        }
    }
    return null; // Bin not found
}

/**
 * Create a new bin with the specified name.
 * @param {string} binName - The name for the new bin.
 * @returns {ProjectItem|null} - Returns the newly created bin or null if creation failed.
 */
function createBin(binName) {
    var existingBin = findBinByName(binName);

    if (!existingBin) {
        // Create the new bin if it doesn't already exist
        var newBin = app.project.rootItem.createBin(binName);
        return newBin; // Return the new bin
    } else {
        return existingBin; // Return the existing bin
    }
}

// Function to add a marker at a given time in the sequence
function addMarkerAtTime(sequence, seconds, markerName) {
    if (markerExistsAtTime(sequence, seconds)) {
        // do nothing
    } else {
        var markers = sequence.markers;
        var newMarker = markers.createMarker(seconds);
        newMarker.name = markerName;
    }
}

function markerExistsAtTime(sequence, seconds) {
    var markers = sequence.markers;

    for (var i = 0; i < markers.length; i++) {
        var markerTime = markers[i].start.seconds; // Get the marker start time in ticks
        // Check if the marker's start time matches the specified time
        if (markerTime === seconds) {
            return true; // Marker exists at this time
        }
    }
    return false; // No marker found at this time
}


function extractClipWidthAndHeight(clip) {
    // Get the associated project item (the source of the clip in the project panel)
    var projectItem = clip.projectItem;

    if (projectItem) {
        // Get the project's XMP metadata
        var xmpMetadata = projectItem.getXMPMetadata();
        var mediaPath = projectItem.getMediaPath();
        var footageInfo = projectItem.get
        if (xmpMetadata) {
            // Look for the "CreateDate" in the XMP metadata
            // <tiff:ImageWidth>3072</tiff:ImageWidth>
            var widthRegEx = /<tiff:ImageWidth>([^<]+)<\/tiff:ImageWidth>/;
            var match = widthRegEx.exec(xmpMetadata);

            var lengthRegEx = /<tiff:ImageLength>([^<]+)<\/tiff:ImageLength>/;
            var match2 = lengthRegEx.exec(xmpMetadata);

            var width, length;

            if (match) {
                width = match[1];
            }

            if (match2) {
                length = match2[1];
            }

            return [width, length];
        }
    }
}