import LoginForm from "./components/LoginForm.js";
import React from "react";
import {Grid} from "@material-ui/core";
import { Link } from "react-router-dom";
import Button from '@material-ui/core/Button'
import Container from '@material-ui/core/Container'

import {  ThemeProvider, createMuiTheme} from '@material-ui/core/styles'
import Box from '@material-ui/core/Box'
import { blue } from '@material-ui/core/colors'
import Typography from '@material-ui/core/Typography'
import { boxShadows } from '@material-ui/core/shadows'

const theme = createMuiTheme({
    typography: {
        h1: {
            fontSize: 36,
        },
        h2: {
            fontSize: 18,
        },
    },
    palette: {
        primary: {
            main: blue[500]
        }
    }
})


export default function Login() {
    return (
        <Box component = "span" m = {1} boxShadow ={3}>
            <Container maxWidth = "xs">
                <ThemeProvider theme = {theme}>
                    <Grid style={{textAlign: "center"}}>
                        <Typography variant = "h1">
                            Let's get started!
                        </Typography>
                        <Typography variant = "h2">
                            Sign in to your account.
                        </Typography>
                        <LoginForm />
                        <Link to="/signup">No account? Sign up here</Link>
                        <div>
                        </div>
                        <Button variant = "contained" color = "primary">
                            Login
                        </Button>
                        <div>
                        </div>
                        <Button variant = "contained" color = "primary">
                            Play as guest
                        </Button>
                    </Grid>
                </ThemeProvider>
            </Container>
        </Box>
    )
}
