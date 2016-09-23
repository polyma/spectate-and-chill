import React from 'react'
import ReactDOM from 'react-dom'

import {Logo} from "./components/Logo.jsx"
import {NavBar} from "./components/NavBar.jsx"
import StreamsBoxContainer from './components/StreamsBox'
import {SummonerSearch} from "./components/SummonerSearch.jsx"
import {About} from "./components/About.jsx"
import {TwitchWidget} from "./components/TwitchWidget.jsx"
import {Loading} from "./components/Loading.jsx"

const reduxStore = require('./store');
import { Provider, connect } from 'react-redux'

var io = require('socket.io-client');
import {receiveStreams, disconnect, newSocket, getRecommendations, newSocketMessage} from './actions/SocketActionCreators';
import {setUserId, backendSwitch} from './middleware/socketMiddleware';

var Content = React.createClass({
    getInitialState: function() {
       return {
           loading: false,
           showRecommendations: false,
           showTwitchWidget: false,
           error: null,
           summonerNameResult: null,
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
       reduxStore.dispatch(newSocketMessage(JSON.parse(msg)));
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
      this.setState({loading: true, error: null}, function() {
        $.ajax({
          url: window.serverUrl + '/summoner?summonerName=' + summonerName + "&region=" + region,
          success: function(data) {
            this._successfulSummonerRequest(data);
            //Now get the recommendations
            this.props.requestReccos(summonerName, region);
          }.bind(this),
          error: function(xhr, err) {
            if(xhr.status === 404) {
              this._setError('Summoner not found');
            }
            else {
              this._setError(err);
            }
          }.bind(this),
          complete: function() {
            this.setState({
                loading: false,
            });
          }.bind(this),
        })
      });
    },

    _setError(err) {
      this.setState({
        error: err,
      })
    },

    _successfulSummonerRequest: function(data) {
        this.setState({
            loading: false,
        });
    },

    render: function() {
      // return(<div className="row">
      //   <SummonerSearch getSummonerData={this._getSummonerData}/>
      //   <StreamsBoxContainer/>
      // </div>)
        if (!this.state.loading) {
            if (this.props.streams.size > 0) {
                $("#bgvid").addClass("hidden");
                return (
                    <div className="row">
                      <NavBar />
                      <StreamsBoxContainer/>
                    </div>
                )
            } else if (this.state.showTwitchWidget){
                $("#bgvid").addClass("hidden");
                return (
                    <div className="row">
                      <NavBar />
                      <TwitchWidget />
                      <StreamsBoxContainer/>
                    </div>
                )
            } else {
                $("#bgvid").removeClass("hidden");
                return (
                    <div className="row">
                      <Logo />
                      <SummonerSearch getSummonerData={this._getSummonerData}/>
                      <About />
                    </div>
                )
            }
        } else {
            $("#bgvid").addClass("hidden");
            return (
                <div className="row">
                  <NavBar />
                  <Loading />
                </div>
            )
        }
    }
});

const mapStateToProps = (state) => {
  return {
      streams: state.get('streams'),
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
