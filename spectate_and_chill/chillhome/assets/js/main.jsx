import React from 'react'
import ReactDOM from 'react-dom'
import Loader from 'react-loaders'

import {NavBar} from "./components/NavBar.jsx"
import {SummonerSearch} from "./components/SummonerSearch.jsx"
import {About} from "./components/About.jsx"
import {TwitchWidget} from "./components/TwitchWidget.jsx"

const reduxStore = require('./store');
import { Provider, connect } from 'react-redux'

var io = require('socket.io-client');
import {receiveStreams, disconnect, newSocket} from './actions/SocketActionCreators';
import {setUserId, backendSwitch} from './middleware/socketMiddleware';

var Content = React.createClass({
    getInitialState: function() {
       return {
           loading: false,
           showVideo: true,
           showRecommendations: false,
           showTwitchWidget: false
       };
   },

   componentDidMount: function() {
     /*
       SET UP SOCKET CONNECTION
     */
     let socket = io.connect('ws://localhost:8080'); //NOTE: need to send user id for this to work
     socket.on('connect', function() {
       console.log('connected to server!');
       reduxStore.dispatch(newSocket(socket));
       //TODO: remove this
       setUserId('21505497_euw');
     });
     socket.on('disconnect', function() {
       reduxStore.dispatch(disconnect());
     });

     socket.on('message', function(msg) {
       console.log('received message!', msg);
       backendSwitch(msg);
     });
   },

   _showVideo: function() {
        this.setState({ showVideo: true }, function() {

        });
    },



    _setLoading : function(data) {
        $.ajax({
            url: this.props.url,
            dataType: 'json',
            cache: false,
            success: function(data) {
                this.setState({ loading: true });
            }.bind(this),
            error: function(xhr, status, err) {
                console.error(this.props.url, status, err.toString());
            }.bind(this)
        });
    },

    _setTwitchVideo: function() {
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
