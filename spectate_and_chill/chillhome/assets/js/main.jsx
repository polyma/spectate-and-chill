import React from 'react'
import ReactDOM from 'react-dom'
import ReactLoader from 'react-loader'

import {NavBar} from "./components/NavBar.jsx"
import {SummonerSearch} from "./components/SummonerSearch.jsx"

var Content = React.createClass({
    render: function() {
        return (
            <div  className="row">
            <h1>Spectate and Chill</h1>
                <NavBar/>
                <SummonerSearch/>
            </div>
        );
    }
});
ReactDOM.render(
    <Content/>, document.getElementById('root'));
