import React from 'react'
import ReactDOM from 'react-dom'
import ReactLoader from 'react-progress-label'

import {NavBar} from "./components/NavBar.jsx"
import {SummonerSearch} from "./components/SummonerSearch.jsx"

const reduxStore = require('./store');
import { Provider } from 'react-redux'

var Content = React.createClass({
    getInitialState: function() {
       return {
           loading: false,
           showVideo: false,
       };
   },

   _showVideo: function() {
        this.setState({ showVideo: true }, function() {
            this.setTimeout(function() {
                this.setState({ loading: false });
            }.bind(this), 1000 / 60);
        });
    },

    _setLoading: function() {
        this.setState({ setLoading: true }, function() {
            this.setTimeout(function() {
                this.setState({ loading: false });
            }.bind(this), 1000 / 60);
        });
    },

    render: function() {
        return (
            <div className="row">
                <NavBar/>
                <SummonerSearch setLoading={this._setLoading}/>
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
