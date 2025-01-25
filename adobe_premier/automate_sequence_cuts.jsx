// https://ppro-scripting.docsforadobe.dev/item/trackitem.html
#include "./utils.jsx"

// Loop through each video track in the sequence\
var activeSequence = getActiveSequence();
var videoTracks = activeSequence.videoTracks;
var audioTracks = activeSequence.audioTracks;
var track = videoTracks[0];
var audioTrack = audioTracks[0];

function deleteAllClipsFromSequence(sequence) {
    // Delete all clips from video tracks
    for (var i = 0; i < sequence.videoTracks.numTracks; i++) {
        var videoTrack = sequence.videoTracks[i];

        for (var j = videoTrack.clips.numItems - 1; j >= 0; j--) {  // Loop backwards to avoid index issues
            var videoClip = videoTrack.clips[j];
            videoClip.remove(true, true);  // Remove the video clip
        }
    }

    // Delete all clips from audio tracks
    for (var i = 0; i < sequence.audioTracks.numTracks; i++) {
        var audioTrack = sequence.audioTracks[i];

        for (var j = audioTrack.clips.numItems - 1; j >= 0; j--) {  // Loop backwards to avoid index issues
            var audioClip = audioTrack.clips[j];
            audioClip.remove(true, true);  // Remove the audio clip
        }
    }
}

function rippleDeleteClip(clip) {
    clip.remove(true, true);

    audioClip = getLinkedAudioFromClip(clip);

    // get the corresponding audioClip
    audioClip.remove(true, true);
}

function getSequenceByName(sequenceName) {
    var sequences = app.project.sequences; // Get all sequences
    for (var i = 0; i < sequences.numSequences; i++) {
        var sequence = sequences[i];
        if (sequence.name === sequenceName) {
            return sequence; // Return the sequence if the name matches
        }
    }
    return null; // Return null if sequence is not found
}

/**
 * Function to copy an existing sequence
 * @param {String} originalSequenceName - The name of the sequence to copy
 * @param {String} newSequenceName - The name for the new copied sequence
 */
function copySequence(originalSequence, newSequenceName) {
    var project = app.project;
    
    if (originalSequence) {
        // first search the sequence by name
        var existingSequence = getSequenceByName(newSequenceName);
        
        if (existingSequence) {
            return existingSequence;
        } else {
            // Duplicate the original sequence
            originalSequence.clone();
            
            // get the new sequence by name
            var copySequenceName = originalSequence.name + " Copy";
        
            var project = app.project;
                
            // Find the original sequence by name
            var newSequenceItem = getSequenceByName(copySequenceName);
            
            // delete all clips from copied sequence
            deleteAllClipsFromSequence(newSequenceItem);
            
            if (newSequenceItem) { 
                newSequenceItem.name = newSequenceName;
                targetSequence = newSequenceItem;
                return newSequenceItem;
            }
        }
        
        return null;
    }
    return null
}

function assembleCutFromMarkers(duration, position) {
    // loop through all markers in the first clip of the "track". Split the duration into 2.
    // At each marker set "markerTimePoint", and create markerCutStart = markerTimePoint - duration / 2, markerCutEnd = markerTimePoint + duration / 2
    // From markerCutStart and markerCutEnd, do a razer cut
    // After the razer cut, go to the previous clip before the razor cut, and delete it
    
    var sourceSequence = getActiveSequence();
    $.writeln("Copying Source sequence: " + sourceSequence.name);
    // var targetSequence = copySequence(activeSequence, activeSequence.name + "_cut");
    var targetSequence = getSequenceByName(sourceSequence.name + "_cut");
    
    var clips = sourceSequence.videoTracks[0].clips;
    
    for (var j = 0; j < clips.length; j++) {
        $.writeln("Processing clip " + j + " of " + clips.length);
        var clip = sourceSequence.videoTracks[0].clips[j];

        var clipSpeed = clip.getSpeed();

        // correct start and end points for clipSpeed
        var clipStart = clip.inPoint.seconds * clipSpeed;
        var clipEnd = clip.outPoint.seconds * clipSpeed;
        
        
        var markers = clip.projectItem.getMarkers();

        if (markers && markers.numMarkers > 0) {
            // Split the duration in half
            var halfDuration = duration / 2;

            // Loop through each marker
            for (var i = 0; i < markers.numMarkers; i++) {
                var marker = markers[i]; // Get the current marker
                var markerTimePoint = marker.start.seconds; // Get the marker's time in ticks
                if (!(marker.start.seconds > clipStart && marker.start.seconds < clipEnd)) {
                    continue;
                }

                // Calculate the start and end points for the razor cut
                var markerCutStart = markerTimePoint - halfDuration;
                var markerCutEnd = markerTimePoint + halfDuration;
                var targetVideoTrack = targetSequence.videoTracks[0];

                clip.projectItem.setInPoint(markerCutStart, 4);
                clip.projectItem.setOutPoint(markerCutEnd, 4);
                
                var lastClip = targetVideoTrack.clips[targetVideoTrack.clips.numItems - 1]
                if (lastClip) {
                    lastClipEnd = lastClip.end.seconds;
                } else {
                    lastClipEnd = 0;
                }

                targetVideoTrack.insertClip(clip.projectItem, lastClipEnd);
            }
        }
    }
    alert("All done!");
}

function getClipAtTimepoint(activeSequence, timePoint) {
    // Loop through each video track in the sequence
    var videoTracks = activeSequence.videoTracks;
    var clipOut = null;
    var clipIdx = null;

    var track = videoTracks[0];

    // Loop through each clip in the track
    for (var j = 0; j < track.clips.length; j++) {
        var clip = track.clips[j];

        // Check if the clip's start time is after the marker's time
        if (clip.start.seconds >= timePoint) {
            clipOut = clip;
            clipIdx = j;
            break;
        }
    }

    return { clip: clipOut, clipIdx: clipIdx };
}

// Function to perform a razor cut at a specific time point on a track
function razorCutAt(track, timePoint) {
    // Loop through the clips on the track
    for (var i = 0; i < track.clips.numItems; i++) {
        var clip = track.clips[i];
        var audioClip = audioTrack.clips[i];
        
        // Check if the current time is within the clip's range
        if (clip.start.seconds <= timePoint && clip.end.seconds >= timePoint) {
            // Get the clip's end time before splitting
            var originalEnd = clip.end;

            // Modify the end time of the original clip
            clip.end = timePoint;
            audioClip.end = timePoint;

            var timeDiff = timePoint - clip.inPoint.seconds;

            // Create a duplicate of the clip
            track.insertClip(clip.projectItem, timePoint);
            // audioTrack.insertClip(audioClip.projectItem, timePoint);
            var newClipObj = getClipAtTimepoint(activeSequence, clip.end.seconds);
            var newClip = newClipObj.clip
            var newClipIdx = newClipObj.clipIdx

            newClip.inPoint = clip.end.seconds;
            audioTrack.clips[newClipIdx].inPoint = clip.end.seconds;

            // newClip.end = originalEnd;

            break; // Exit after splitting the first active clip
        }
    }

    return { beforeClip: clip, afterClip: newClip };
}

// Function to delete the clip before the cut point
function deleteClipBeforeCut(track, cutPoint) {
    for (var i = 0; i < track.clips.numItems; i++) {
        var clip = track.clips[i];
        
        // If the clip ends at or before the cut point, it's the one before the razor cut
        if (clip.end.seconds <= cutPoint) {
            clip.remove(); // Delete the clip
            break;
        }
    }
}

assembleCutFromMarkers(2.83, "middle")

