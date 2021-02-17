import React,{ Component } from 'react';
import axios from 'axios';
import './Main.css'

axios.defaults.baseURL = 'http://localhost:8000';

export default class Main extends Component {

    render() {
        return(
            <div>
                hello
            </div>
        )
    }
}