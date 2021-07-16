import React from "react";
import {Link, Redirect} from 'react-router-dom';
import { TextField, Button, Box } from "@material-ui/core";
import { makeStyles } from '@material-ui/core/styles';
import LoginFormBl from "./bl.js";
import Typography from '@material-ui/core/Typography';

const useStyles = makeStyles((theme) => ({
    margin: {
        margin: theme.spacing(1),
    },
}));


export default function LoginForm() {
    const classes = useStyles();
    const { loggedIn, handleChange, handleSubmit, loginFailed } = LoginFormBl();

    return (
        <>
            {loggedIn ? <Redirect to="/" /> :
            <form onSubmit={handleSubmit}>
                <div>
                    <TextField id = "filled-basic" label = "Filled" variant = "filled" type="text" name="username" label="Username" onChange={handleChange} />
                </div>
                <div>
                    <TextField id = "filled-basic" label = "Filled" variant = "filled" type="password" name="password" label="Password" onChange={handleChange} />
                </div>
                <Typography variant = "h3" className = {classes.margin}>
                    No account? Sign up
                    <Link to="/signup"> here.</Link>
                </Typography>
                <br></br>
                <Button type="submit" variant = "contained" color = "primary" className = {classes.margin} style = {{maxWidth: '150px', minWidth: '150px'}}>Login</Button>
                {loginFailed && <p>Invalid login</p>}
                <div>
                </div>
                <Button variant = "contained" color = "secondary" style = {{maxWidth: '150px', minWidth: '150px'}}>
                    Play as guest
                </Button>
                <br></br>
                <br></br>
                <Typography variant = "h3">
                    <Link to = "https://github.com/JJamali/Intervals"> View GitHub Repository</Link>
                </Typography>
            </form>}
        </>
    );
}
