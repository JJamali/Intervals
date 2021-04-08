import { useState } from "react";
import PropTypes from "prop-types";
import { Button, Grid, ButtonBase } from "@material-ui/core";
import { withStyles, makeStyles } from "@material-ui/core/styles";


const useStyles = makeStyles({
    disabled: {
        "&$disabled": {
            backgroundColor: props => props.isCorrect ? "green" : "red",
            color: "black"
        },
    }
})


const AnswerButton = (props) => {
    const classes = useStyles(props);

    return (
        <Button
            value={props.answer}
            variant="contained"
            onClick={props.onClick}
            disabled={props.answered}
            classes={{ disabled: classes.disabled }}>
            {props.answer}
        </Button>
    )
}

export default AnswerButton;
