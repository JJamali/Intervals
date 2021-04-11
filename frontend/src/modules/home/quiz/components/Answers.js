import { Grid } from "@material-ui/core";
import AnswerButton from "./AnswerButton.js";



export default function Answers({question, handleSubmit, correctAnswer, answered}) {
    return (
        <div className="answers">
            <Grid container direction="column" alignItems="center" spacing={2}>
                {question.answers && question.answers.map((answer, index) => {
                    const isCorrect = answer === correctAnswer;
                    return (
                        <Grid item key={index}>
                            <AnswerButton answer={answer} onClick={handleSubmit} isCorrect={isCorrect} answered={answered} />
                        </Grid>
                    )
                })}
            </Grid>
        </div>
    );
}
