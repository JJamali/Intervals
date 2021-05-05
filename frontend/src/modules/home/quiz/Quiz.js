import React from "react";
import { makeStyles } from "@material-ui/core/styles";
import { Box, Paper, Button, Grid } from "@material-ui/core"
import QuizBl from "./bl.js";
import Answers from "./components/Answers.js";
import PlayButton from "./components/PlayButton.js";
import RecentResults from "./components/RecentResults.js";
import { UserContext } from "modules/app/context/UserContext.js";
import "./Quiz.css";


const useStyles = makeStyles({
    root: {
        width: "50vw",
    },
    quiz: {
        width: "80%",
        margin: "auto",
        marginBottom: 10,
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

export default function Quiz() {
    const classes = useStyles();
    const { question, recentResults, handleSubmit, correctAnswer, answered, goNext } = QuizBl();

    return (
        <div className={classes.root}>
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
            <RecentResults recentResults={recentResults} />
        </div>
    );
}
