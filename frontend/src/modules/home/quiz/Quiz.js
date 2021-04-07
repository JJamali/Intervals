import React from "react";
import { makeStyles } from '@material-ui/core/styles';
import { Paper, Button, Grid, LinearProgress } from "@material-ui/core"
import QuizBl from "./bl.js";


const RecentResults = ({recentResults}) => {
    const count = recentResults.reduce((acc, curr) => acc + (curr ? 1 : 0));
    const progress = 100 * count/20;
    console.log(count);

    return (
        <>
            <Grid container direction="row" spacing={2}>
                {recentResults.map((result, index) => {
                    const display = result ? "✓" : "x";
                    const color = result ? "green" : "red";
                    return (
                        <Grid item key={index}>
                            <Paper style={{color: color}}>{display}</Paper>
                        </Grid>
                    )
                })}
            </Grid>
            <LinearProgress variant="determinate" value={progress} style={{margin: "10px"}} />
        </>
    )
}


export default function Quiz() {
    const { question, recentResults, handleSubmit } = QuizBl();

    return (
        <Paper>
            <div>
                <b style={{paddingRight: "20px"}}>{question.question}</b>
                <span>From {question.first_note} to {question.second_note}</span>
            </div>
            <div>
                {question.answers && question.answers.map((answer, index) =>
                    <Button value={answer} onClick={handleSubmit} key={index}>
                        {answer}
                    </Button>
                )}
            </div>
            <RecentResults recentResults={recentResults} />
        </Paper>
    );
}
