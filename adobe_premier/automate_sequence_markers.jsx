#include "./utils.jsx"

function getFirstClipFromMarker(activeSequence, currentMarker) {
    // Loop through each video track in the sequence
    var videoTracks = activeSequence.videoTracks;
    var clip = null;

    var track = videoTracks[0];

    // Loop through each clip in the track
    for (var j = 0; j < track.clips.length; j++) {
        var clip = track.clips[j];

        // Check if the clip's start time is after the marker's time
        if (clip.start.seconds > currentMarker.start.seconds) {
            clip = clip;
            break;
        }
    }

    return clip;
}

function extractCreationDateFromClip(clip) {
    // Get the associated project item (the source of the clip in the project panel)
    var projectItem = clip.projectItem;

    if (projectItem) {
        // Get the project's XMP metadata
        var xmpMetadata = projectItem.getXMPMetadata();

        if (xmpMetadata) {
            // Look for the "CreateDate" in the XMP metadata
            var createDateRegex = /<xmp:CreateDate>([^<]+)<\/xmp:CreateDate>/;
            var match = createDateRegex.exec(xmpMetadata);

            if (match) {
                var creationDate = match[1];
                return getFormattedDate(creationDate);  
            }
        }
    }
}

function convertMarkerToSequence(binName) {
    var activeSequence = getActiveSequence();
    if (activeSequence) {
        // create a bin
        var binName = activeSequence.name + "_subClips";
        var bin = createBin(binName);

        // Get markers from the sequence
        var markers = activeSequence.markers;

        if (markers.numMarkers > 1) {
            var currentMarker = markers.getFirstMarker();
            var markerCount = 1;

            while (currentMarker !== undefined) {
                // get the creation date from the first clip
                var firstClipFromMarker = getFirstClipFromMarker(activeSequence, currentMarker);
                var firstClipCreationDate = extractCreationDateFromClip(firstClipFromMarker)

                if (!getFirstClipFromMarker || !firstClipCreationDate){
                    alert("ERROR: could not find first clip from marker");
                    break;
                }

                // Find next marker
                var nextMarker = markers.getNextMarker(currentMarker);
                var markerName = currentMarker.name;

                if (nextMarker !== undefined) {
                    // // Set in and out points between the markers
                    activeSequence.setInPoint(currentMarker.start.ticks);
                    activeSequence.setOutPoint(nextMarker.start.ticks);

                    
                    // // Create a new sequence for this section
                    var sequenceName = firstClipCreationDate + "_Clip" + padWithZeros(markerCount, 2);
                    // if (markerName) sequenceName += "_" + markerName;

                    var newSequence = activeSequence.createSubsequence();
                    newSequence.name = sequenceName;
                    
                    markerCount++;
                    // Move to the next marker
                    currentMarker = markers.getNextMarker(nextMarker);
                }
            }
        }
    }
}


function getLastClip(activeSequence) {
    if (activeSequence) {
        var videoTrack = activeSequence.videoTracks[0]; // Adjust the track index if needed

        if (videoTrack.clips.length > 0) {
            var lastClip = videoTrack.clips[videoTrack.clips.length - 1]; // Get the last clip
            return lastClip;
        }
    }
}

function addMarkers() {
    var activeSequence = getActiveSequence();
    var videoTrack = activeSequence.videoTracks[0]; // Adjust if needed for different tracks
    
    if (videoTrack.clips.length > 1) {
        var previousClipEnd = null;
        var markerGroup = 1;
        for (var i = 0; i < videoTrack.clips.length - 1; i++) {
            var currentClip = videoTrack.clips[i];
            var nextClip = videoTrack.clips[i + 1];
            
            // Calculate the end time of the current clip
            var currentClipEnd = currentClip.end.seconds;

            // Calculate the start time of the next clip
            var nextClipStart = nextClip.start.seconds;

            // If there is a gap between current and next clip
            if (currentClipEnd < nextClipStart) {
                // Add a marker at the end of the current clip (end of group)
                addMarkerAtTime(activeSequence, currentClipEnd, "End");

                // Add a marker at the start of the next clip (start of next group)
                addMarkerAtTime(activeSequence, nextClipStart, "Start");
            }
        }
        
        // Add a marker at the beginning of the first clip if needed
        var firstClipStart = videoTrack.clips[0].start.seconds;
        addMarkerAtTime(activeSequence, firstClipStart, "Start");

        // get the last clip and add a marker
        var lastClip = getLastClip(activeSequence);
        addMarkerAtTime(activeSequence, lastClip.end.seconds, "End");
    }
}



addMarkers();
convertMarkerToSequence();