import React, { Component } from "react";
import CreateUserPage from "./User/HomePage";
import LoginPage from "./Market";
import { BrowserRouter as Router, Switch, Route, Link, Redirect } from "react-router-dom";

export default class HomePage extends Component {
    constructor(props) {
        super(props)
    }

    render() {
        return (
            <Router>
                <Switch>
                    <Route exact path="/">
                        <p>This is the homepage</p>
                        </Route>
                    <Route path="/create-user" component= {CreateUserPage}></Route>
                    <Route path="/login" component= {LoginPage}></Route>
                </Switch>
            </Router>
        );
    }
}