import React from 'react'
import ReactDOM from 'react-dom'

import {Logo} from "./components/Logo.jsx"
import StreamsBoxContainer from './components/StreamsBox'
import {SummonerSearch} from "./components/SummonerSearch.jsx"
import {About} from "./components/About.jsx"
import {TwitchWidget} from "./components/TwitchWidget.jsx"
import {Loading} from "./components/Loading.jsx"

const reduxStore = require('./store');
import { Provider, connect } from 'react-redux'

var io = require('socket.io-client');
import {receiveStreams, disconnect, newSocket, getRecommendations} from './actions/SocketActionCreators';
import {setUserId, backendSwitch} from './middleware/socketMiddleware';

var Content = React.createClass({
    getInitialState: function() {
       return {
           loading: false,
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

    _setLoading : function(data) {

    },

    _setTwitchVideo: function() {
        this.setState({ setTwitchWidget: true }, function() {

        });
    },

    _getSummonerData: function(summonerName, region) {
      console.log('Beginning summoner fetch...', summonerName, region);
      this.setState({loading: true}, function() {
        this._successfulSummonerRequest();
        //Now get the recommendations
        this.props.requestReccos(summonerName, region);
      });
    },

    _successfulSummonerRequest: function() {
        this.setState({
            loading: true,
        });
    },

    render: function() {
        if (!this.state.loading) {
            return (
                <div className="row">
                    <Logo />
                    <SummonerSearch getSummonerData={this._getSummonerData}/>
                    <About />
                    <StreamsBoxContainer/>
                </div>
            )
        } else {
            return (
                <div className="row">
                    <Loading />
                </div>
            )
        }
    }
});

const mapStateToProps = (state) => {
  return {
  }
}
const mapDispatchToProps = (dispatch) => {
  return {
    requestReccos: (sn, reg) => {
      dispatch(getRecommendations(sn, reg))
    }
  }
}

var ContentContainer = connect(
  mapStateToProps,
  mapDispatchToProps,
)(Content)

ReactDOM.render(
    <Provider store={reduxStore}>
      <ContentContainer/>
    </Provider>
    , document.getElementById('root')
);
