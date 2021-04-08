import { useState } from "react";
import PropTypes from "prop-types";
import { Button, Grid, ButtonBase } from "@material-ui/core";
import { makeStyles } from "@material-ui/core/styles";
import AnswerButton from "./AnswerButton.js";



export default function Answers({question, handleSubmit, correctAnswer, answered}) {
    return (
        <div className="answers">
            <Grid container direction="column" alignItems="center" spacing={2}>
                {question.answers && question.answers.map((answer, index) => {
                    console.log(answer, correctAnswer);
                    const isCorrect = answer == correctAnswer ? true : false;
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
