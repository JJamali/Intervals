import React from "react";
import { makeStyles } from "@material-ui/core/styles";
import { Paper, Grid, Divider } from "@material-ui/core";
import clsx from "clsx";
import {UserContext} from "../../../app/context/UserContext";


const useStyles = makeStyles({
    paper: {
        overflow: "hidden",
        backgroundColor: "darkgray",
        borderColor: "black",
        borderWidth: 1,
    },
    item: {
        width: props => `${props.segmentWidth}%`,
    },
    segment: {
        width: "100%",
        height: props => props.height,
    },
    correct: {
        backgroundColor: "green",
    },
    incorrect: {
        backgroundColor: "white",
    },
    empty: {
        backgroundColor: "transparent",
    },
    divider: {
        backgroundColor: "#222",
    },
})


const RecentResults = ({numSegments=20, height=16}) => {
    const { user } = React.useContext(UserContext);
    const segmentWidth = 100 / numSegments;
    const classes = useStyles({segmentWidth, height});

    // extend results with nulls to have a length of numSegments
    let extendedResults = [...user.stats.recentResults.recent_results];
    for (let i = 0; i < numSegments - user.stats.recentResults.recent_results.length; i++) {
        extendedResults.push(null);
    }

    return (
        <Paper elevation={3} className={classes.paper}>
            <Grid container  direction="row" wrap="nowrap" height={height}>
                {extendedResults.map((r, i) => {
                    let cls;
                    if (r === null) {
                        cls = classes.empty;
                    } else if (r) {
                        cls = classes.correct;
                    } else {
                        cls = classes.incorrect;
                    }
                    return (
                        <React.Fragment key={i}>
                            {i !== 0 && <Divider orientation="vertical" flexItem className={classes.divider} />}
                            <Grid item className={classes.item}>
                                <Paper elevation={0} square className={clsx(classes.segment, cls)} />
                            </Grid>
                        </React.Fragment>
                    );
                })}
            </Grid>
        </Paper>
    );
}


export default RecentResults;
