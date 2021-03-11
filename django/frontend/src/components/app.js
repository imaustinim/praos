import React, { Component } from "react";
import { render } from "react-dom";
import HomePage from "./HomePage";
import Market from "./Market";
import UserHomePage from "./User/HomePage";

export default class App extends Component {
    constructor(props) {
        super(props);
    }
    
    render() {
        return (
            <div>
                <HomePage></HomePage>
            </div>
        )
    }
}

const appDiv = document.querySelector("#app");
render(<App/>, appDiv);