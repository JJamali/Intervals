import React from "react";
import { makeStyles } from "@material-ui/core/styles";
import { Box, Paper, Button, Grid, LinearProgress } from "@material-ui/core"
import QuizBl from "./bl.js";
import Answers from "./components/Answers.js";
import PlayButton from "./components/PlayButton.js";
import "./Quiz.css";


const useStyles = makeStyles({
    quiz: {
        width: "300px",
    },
    correct: {
        width: "30px",
        textAlign: "center",
        backgroundColor: "green",
    },
    incorrect: {
        width: "30px",
        textAlign: "center",
        backgroundColor: "red",
    },
})


const RecentResults = ({recentResults}) => {
    const classes = useStyles();

    const count = recentResults.reduce((acc, curr) => acc + (curr ? 1 : 0));
    const progress = 100 * count/20;
    console.log(count);

    return (
        <>
            <Grid container direction="row" spacing={2}>
                {recentResults.map((result, index) => {
                    if (result) {
                        return (
                            <Grid item key={index}>
                                <Paper className={classes.correct}>✓</Paper>
                            </Grid>
                        )
                    }
                    else {
                        return (
                            <Grid item key={index}>
                                <Paper className={classes.incorrect}>x</Paper>
                            </Grid>
                        )
                    }
                })}
            </Grid>
        </>
    )
}


export default function Quiz() {
    const classes = useStyles();
    const { question, recentResults, handleSubmit, correctAnswer, answered, goNext } = QuizBl();

    return (
        <Paper className={classes.quiz}>
            <div className="quiz-header">
                <div className="question-text">{question.question_text}</div>
                <div className="interval">
                    <Grid container direction="row" alignItems="center">
                        <p>Play notes:</p>
                        <PlayButton first={question.first_note} second={question.second_note} />
                    </Grid>
                </div>
            </div>
            <Answers question={question} handleSubmit={handleSubmit} correctAnswer={correctAnswer} answered={answered} />
            <Box className="right-box">
                <Button disabled={!answered} onClick={goNext}>NEXT</Button>
            </Box>
        </Paper>
    );
}
