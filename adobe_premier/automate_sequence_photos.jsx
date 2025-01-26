// https://ppro-scripting.docsforadobe.dev/item/trackitem.html
#include "./utils.jsx"
var activeSequence;
var track;
var globalZoomDirection = "in";
var globalZoomStrength = 0.05;
var music_bpm = 85;
var beats_sustain = 4;
var globalZoomDuration = 60/music_bpm * beats_sustain; 


function processPhotos() {
    activeSequence = getActiveSequence();

    if (!activeSequence) {
        alert("No active sequence found.");
        return;
    }

    track = activeSequence.videoTracks[0];
    
    // Loop through each clip in the track
    for (var j = 0; j < track.clips.numItems; j++) {
        var clip = track.clips[j];
        if (isPhoto(clip)) {
            // Handle the photo clip (e.g., log its name or index)
            var clipName = clip.projectItem.name;
            var dim = extractClipWidthAndHeight(clip);
            // Check if dim[0] is NaN
            if (isNaN(dim[0])) {
                alert("Skipping clip due to invalid dimensions.");
                continue; // Skip processing this clip
            }
            if (dim[0] < dim[1]) // portrait
                scale = 1080 / dim[0] * 100 * 1.2;
            else // landscape
                scale = 1080 / dim[0] * 100 * 1.2;
        
            setClipScale(clip, scale);
            setZoomEffectOnImage(clip, globalZoomDirection, globalZoomStrength, globalZoomDuration)
        }
    }
    alert("All done!");

}

// Function to check if a clip is a photo based on its file extension
function isPhoto(clip) {
    var filePath = clip.projectItem.getMediaPath().toLowerCase();
    var parts = filePath.split(".");
    var extension = parts[parts.length - 1].toLowerCase();

    const photoExtensions = ['jpg', 'jpeg', 'png', 'tiff', 'bmp'];
    var isPhotoFlag = false;
    for (var i = 0; i < photoExtensions.length; i++) {
        if (extension === photoExtensions[i]) {
            isPhotoFlag = true;
        }
    }
    
    return isPhotoFlag;
}

// Function to set the scale of a clip in a sequence
function setClipScale(clip, scaleValue) {
    var motionComponent = clip.components[1]; // "Motion" component is usually the second component
    
    if (motionComponent && motionComponent.displayName === "Motion") {
        var scaleParam = motionComponent.properties[1]; // "Scale" is usually the second property in "Motion"

        if (scaleParam && scaleParam.displayName === "Scale") {
            scaleParam.setValue(scaleValue, false);
            return true;
        }
    }
    return false;
}

function clear_scale_keyframes(clip) {
     // Get the "Motion" effect's scale property
    var motionEffect = clip.components[1]; // Assuming "Motion" is the second component
    var scaleProperty = motionEffect.properties[1]; // Assuming "Scale" is the second property

    // Check if the "Scale" property has keyframes
    if (scaleProperty.isTimeVarying()) {
        // Get the number of keyframes
        var keyframeCount = scaleProperty.getKeys().length;

        // Loop through and remove all keyframes
        for (var i = keyframeCount - 1; i >= 0; i--) {
            // Remove keyframe at index i
            scaleProperty.removeKey(i);
        }

        // Optional: Disable time-varying (keyframing) for the property if no keyframes remain
        scaleProperty.setTimeVarying(false);
    }
}

function setZoomEffectOnImage(clip, zoomDirection, strength, duration) {  
    /* Take the clip, set it to the duration specified, with ripple edit enabled
    so that any change in duration will automatically ripple the remaining
    clips. For that clip, then get the scale and save it as "initialScale". 
    Calculate "zoomScale" variable using the "strength" variable, which
    is calculated as the % of the "initialScale". So if the strength is 0.1,
    then "zoomScale" variable is 10% more than "initialScale".

    If the zoom direction is "In", create a new keyframe at the 
    beginning on the "Scale" parameter, and set it to "initialScale". 
    Add a key frame at the end of the clip, 
    and set the scale to "zoomScale". 

    If the zoom direction is "out", first set the initial scale to "zoomScale",
    and add a keyframe at the end for the "initialScale". 
    */

    clear_scale_keyframes(clip);
    $.writeln("processing clip: " + clip.name);

    if (!zoomDirection) zoomDirection = "in"; // Default to "in" if not provided
    // Set the duration of the clip and enable ripple edit
    // clip.duration.setinsetInPoint(clip.start.seconds); // Assuming the clip's starting point
    clip.inPoint = clip.start.seconds;
    clip.outPoint = clip.end.seconds;
    duration = clip.end.seconds - clip.start.seconds;
    // rippleEditClip(clip, duration);


    // clip.end = clip.start.seconds + duration;

    // Get the "Motion" effect's scale property
    var motionEffect = clip.components[1]; // Assuming "Motion" is the second component
    var scaleProperty = motionEffect.properties[1]; // Assuming "Scale" is the second property

    // Save the current scale as "initialScale"
    var initialScale = scaleProperty.getValueAtTime(clip.start.seconds); // Get scale at the clip's start

    // Calculate the "zoomScale" based on the strength variable
    var zoomScale;
    zoomScale = initialScale * (1 + strength); // Zoom in (increase scale)
    
    // Enable keyframes for the "Scale" property
    scaleProperty.setTimeVarying(true);

    // Set keyframes based on the zoom direction
    if (zoomDirection === "in") {
        // Zoom in: start at initial scale, end at zoomScale
        scaleProperty.addKey(clip.start.seconds); // Add keyframe at the start
        scaleProperty.setValueAtKey(clip.start.seconds, initialScale); // Set initial scale at the start

        var endTime = clip.start.seconds + duration; // End time based on duration
        scaleProperty.addKey(endTime); // Add keyframe at the end
        scaleProperty.setValueAtKey(endTime, zoomScale); // Set zoom scale at the end
    } else if (zoomDirection === "out") {
        // Zoom out: start at zoomScale, end at initial scale
        scaleProperty.addKey(clip.start.seconds); // Add keyframe at the start
        scaleProperty.setValueAtKey(clip.start.seconds, zoomScale); // Set zoom scale at the start

        var endTime = clip.start.seconds + duration; // End time based on duration
        scaleProperty.addKey(endTime); // Add keyframe at the end
        scaleProperty.setValueAtKey(endTime, initialScale); // Set initial scale at the end
    }
}

function rippleEditClip(clip, duration) {
    var newEnd = clip.start.seconds + duration;
    var timeDiff = newEnd - clip.end.seconds;
    clip.end = newEnd;

    // Loop through all subsequent clips on the same track
    for (var i = 0; i < track.clips.numItems; i++) {
        var followingClip = track.clips[i];
        var audioClip = getLinkedAudioFromClip(activeSequence, followingClip)

        // Move clips that start after the current clip
        if (followingClip.start.seconds > clip.start.seconds) {
            followingClip.move(timeDiff); // Move the start position
            if (audioClip) audioClip.move(timeDiff);
        }
    }
}

function apply_blur_to_landscape_photo(clip) {
    /* Copy the selected clip to Track 2, and remove all keyframes. 
        Take the original clip on Track 1,
        set scale to 90, apply gaussian blur, apply reverse zoom effect
    */
}


processPhotos();