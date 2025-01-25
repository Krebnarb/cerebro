function calculateDuration(fps, bpm, sustain_beats) {
    // Calculate seconds per beat
    const seconds_per_beat = (60 / bpm) * sustain_beats;

    // Separate the whole number and decimal portion of seconds
    const s1 = Math.floor(seconds_per_beat);
    const s2 = seconds_per_beat - s1;

    // Calculate the number of frames
    const frames = Math.floor(fps * s2);

    // Return the formatted response
    return `${s1}:${frames} / ${seconds_per_beat}`;
}

const sustain_beats = [1, 2, 4, 6, 8];
const bpm = 85;
sustain_beats.forEach(beat => {
    const output = calculateDuration(30, bpm, beat);
    console.log(`${beat}: ${output}`);
});