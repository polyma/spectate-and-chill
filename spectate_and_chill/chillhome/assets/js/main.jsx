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
           showRecommendations: false,
           showTwitchWidget: false,
           error: null,
           summonerNameResult: null,
           status: '',
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

    _setTwitchVideo: function() {
        this.setState({ setTwitchWidget: true }, function() {

        });
    },

    _getSummonerData: function(summonerName, region) {
      console.log('Beginning summoner fetch...', summonerName, region);
      this.setState({
        status: 'Grabbing Summoner data',
      })
      this.props.setLoad();
      this.setState({error: null}, function() {
        $.ajax({
          url: window.serverUrl + '/summoner?summonerName=' + summonerName + "&region=" + region,
          success: function(data) {
            this._successfulSummonerRequest(data);
            //Now get the recommendations
            this.setState({
              status: 'Initializing recomendations engine',
            });
            this.props.setLoad();
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
    },

    render: function() {
      // return(<div className="row">
      //   <SummonerSearch getSummonerData={this._getSummonerData}/>
      //   <StreamsBoxContainer/>
      // </div>)
        if (!this.props.isLoading) {
            if (this.props.streams.size > 0) {
                $("#bgvid").addClass("hidden");
                return (
                    <div className="row">
                      <NavBar />
                      <StreamsBoxContainer/>
                    </div>
                )
            } else if (this.state.showTwitchWidget && this.props.stateFul.get('streams')){
                $("#bgvid").addClass("hidden");
                return (
                    <div className="row">
                      <NavBar />
                      <TwitchWidget name={this.stateFul ? this.stateFul.get('topStream') : null}/>
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
                  <Loading status={this.state.status}/>
                </div>
            )
        }
    }
});

const mapStateToProps = (state) => {
  return {
    isLoading: state.get('isLoading'),
    stateFul: state,
    streams: state.get('streams'),
  }
}
const mapDispatchToProps = (dispatch) => {
  return {
    requestReccos: (sn, reg) => {
      dispatch(getRecommendations(sn, reg))
    },
    setLoad: function() {
      dispatch({type: 'SET_LOADING', payload: true})
    },
    unSetLoad: function() {
      dispatch({type: 'UNSET_LOADING', payload: false})
    },
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
