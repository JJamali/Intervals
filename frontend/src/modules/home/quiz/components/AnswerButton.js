import { useState } from "react";
import PropTypes from "prop-types";
import { Button, Grid, ButtonBase } from "@material-ui/core";
import { withStyles, makeStyles } from "@material-ui/core/styles";
//
// const styles = theme => ({
//     button: {
//         root: {
//             background: "red",
//             "&$disabled": {
//                 background: "blue",
//             }
//         },
//     }
// });

const useStyles = makeStyles({
    button: {
    },
    disabled: {
        background: props => props.isCorrect ? "green" : "red",
        "&$disabled": {
            color: "black"
        }
    }
})

//const AnswerButton = Button;

const AnswerButton = (props) => {
    const classes = useStyles(props);

    return (
        <Button onClick={props.onClick} disabled={props.answered} classes={{ root: classes.button, disabled: classes.disabled }}>
            {props.answer}
        </Button>
    )
}
//
// AnswerButton.propTypes = {
//   classes: PropTypes.object.isRequired
// };
//
// export default withStyles(styles)(AnswerButton);
export default AnswerButton;
