import React, { Component } from "react";
import "./App.css";
import {
    BrowserRouter as Router,
    Switch,
    Route
} from "react-router-dom";
import Grid from "@material-ui/core/grid";
import Login from "modules/login/Login.js";
import Signup from "modules/signup/Signup.js";
import Home from "modules/home/Home.js";
import UserProvider from "modules/app/context/UserContext.js";

class App extends Component {


    render() {
        return (
            <Grid container justify="center">
                <Grid item>
                    <Router>
                        <UserProvider>
                            <Switch>
                                <Route exact path="/">
                                    <Home />
                                </Route>
                                <Route path="/login">
                                    <Login />
                                </Route>
                                <Route path="/signup">
                                    <Signup setToken={this.setToken} />
                                </Route>
                            </Switch>
                        </UserProvider>
                    </Router>
                </Grid>
            </Grid>
        );
    }
}

export default App;
