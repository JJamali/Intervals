import LoginForm from "./components/LoginForm.js";
import React from "react";
import {Grid} from "@material-ui/core";
import { Link } from "react-router-dom";
import Button from '@material-ui/core/Button';
import Container from '@material-ui/core/Container';

import {  makeStyles, ThemeProvider, createMuiTheme} from '@material-ui/core/styles';
import {blue, grey} from '@material-ui/core/colors';
import Typography from '@material-ui/core/Typography';
import Paper from '@material-ui/core/Paper';
import Box from '@material-ui/core/Box';

const theme = createMuiTheme({
    typography: {
        h1: {
            fontSize: 36,
        },
        h2: {
            fontSize: 18,
        },
        h3: {
            fontSize: 14,
        },
    },
    palette: {
        primary: {
            main: blue[500]
        },
        secondary: {
            main: grey[500]
        }
    },
})

const useStyles = makeStyles ({
    paper: {
        width: "100%",
        height: "100%",
        backgroundColor: 'blue',
        elevation: '1',
    },
});


export default function Login() {
    const classes = useStyles();

    return (
        <Box display = "flex" justifyContent = "center" alignItems = "center" minHeight = "90vh">
            <Paper classname={classes.paper} elevation = {24}>
                <Box display = "flex" justifyContent = "center" alignItems = "center" minHeight = "80vh" minWidth = "150vh">
                    <Container maxWidth = "lg">
                        <ThemeProvider theme = {theme}>
                            <Grid style={{textAlign: "center"}}>
                                <Typography variant = "h1">
                                    Let's get started!
                                </Typography>
                                <Typography variant = "h2">
                                    Sign in to your account.
                                </Typography>
                                <br></br>
                                <LoginForm />
                            </Grid>
                        </ThemeProvider>
                    </Container>
                </Box>
            </Paper>
        </Box>

    )
}