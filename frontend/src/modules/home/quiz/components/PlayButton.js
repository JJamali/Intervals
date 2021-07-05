import { Button } from "@material-ui/core"
import PlayArrowIcon from "@material-ui/icons/PlayArrow";
import * as Tone from "tone";


const playTone = (first, second) => {
        // Create a synth and connect it to the main output (your speakers)
        const synth = new Tone.Synth().toDestination();
        const now = Tone.now()

        // Play the first and second notes sequentially with the duration of an 8th note
        synth.triggerAttackRelease(first, "8n", now);
        synth.triggerAttackRelease(second, "8n", now + 0.5);
}

const PlayButton = ({first, second}) => {

    return (
        <Button onClick={() => {playTone(first, second)}} color="primary">
            <PlayArrowIcon />
        </Button>
    )
}

export {playTone};
export default PlayButton;
