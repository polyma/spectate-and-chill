import React from 'react'
import ReactDOM from 'react-dom'
import ReactLoader from 'react-loader'

import {NavBar} from "./components/NavBar.jsx"
import {SummonerSearch} from "./components/SummonerSearch.jsx"
import {About} from "./components/About.jsx"

const reduxStore = require('./store');
import { Provider } from 'react-redux'

var Content = React.createClass({
    getInitialState: function() {
       return {
           loading: false,
           showVideo: true,
           showRecommendations: false,
           showTwitchWidget: false
       };
   },

   _showVideo: function() {
        this.setState({ showVideo: true }, function() {

        });
    },

    _setLoading: function(loaded) {
        if (loaded) {
            this.setState({ setLoading: true }, function() {

            });
        }
    },

    _setRecommendatinos: function() {
        this.setState({ showRecommendations: true }, function() {

        });
    },

    _setRecommendatinos: function() {
        this.setState({ setTwitchWidget: true }, function() {

        });
    },

    render: function() {
        return (
            <div className="row">
                <NavBar/>
                <SummonerSearch setLoading={this._setLoading}/>
                <About />
            </div>
        );
    }
});
ReactDOM.render(
    <Provider store={reduxStore}>
      <Content/>
    </Provider>
    , document.getElementById('root')
);
