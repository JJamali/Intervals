import { Button } from "@material-ui/core"
import PlayArrowIcon from "@material-ui/icons/PlayArrow";
import * as Tone from "tone";

const PlayButton = ({first, second}) => {
    const playTone = () => {
        //create a synth and connect it to the main output (your speakers)
        const synth = new Tone.Synth().toDestination();
        const now = Tone.now()

        //play a middle 'C' for the duration of an 8th note
        synth.triggerAttackRelease(first, "8n", now);
        synth.triggerAttackRelease(second, "8n", now + 0.5);
    }

    return (
        <Button onClick={playTone} color="primary">
            <PlayArrowIcon />
        </Button>
    )
}

export default PlayButton;
