import React from "react"

export class SearchInputForm extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            summonerName: '',
            region: 'euw',
            error: null,
        }
        this.changeName = this._changeName.bind(this)
        this.changeRegion = this._changeRegion.bind(this);
        this.validateInput = this._validateInput.bind(this);
        // this.getSummonerData = this._getSummonerData.bind(this);
    }

    _validateInput(e) {
        e.preventDefault();
        this.props.getSummonerData(this.state.summonerName, this.state.region);
        var re = new RegExp("^([\p{L}_. ]+)$");
        if (re.test(this.state.summonerName)) {
          console.log('valid input!');
            this.props.getSummonerData(this.state.summonerName, this.state.region);
        }
        else {
            this.setState({error: 'SUMMONER NAME INCORRECTLY FORMATTED'})
        }
    }

    render() {
        return (
            <div className="inputForm form-horizontal animated fadeInDown">
              <div className="form-group row">
                {this.state.error
                  ? <h2>ERROR {this.state.error}</h2>
                : null}
                <form>
                  <div className="col-xs-6 col-xs-offset-2 ">
                    <input type="text" value={this.state.summonerName} onChange={this.changeName} id="summoner" className="form-control search-bar" placeholder="Summoner name" ></input>
                  </div>
                  <div>
                    <select className="col-xs-2 form-control region-btn" value={this.state.region} onChange={this._changeRegion} >
                      <option value="na">NA</option>
                      <option value="euw">EUW</option>
                      <option value="eune">EUNE</option>
                      <option value="br">BR</option>
                      <option value="kr">KR</option>
                      <option value="lan">LAN</option>
                      <option value="las">LAS</option>
                      <option value="oce">OCE</option>
                      <option value="ru">RU</option>
                      <option value="tr">TR</option>
                    </select>
                  </div>
                  <div className="submit col-xs-1">
                    <button onClick={this.validateInput} type="submit" className="submit-button"><span className="glyphicon glyphicon-search"></span></button>
                    </div>
                    </form>
                </div>
            </div>
        );
    }

    _changeName(e) {
        this.setState({summonerName: e.target.value});
    }

    _changeRegion(e) {
        this.setState({region: e.value});
    }
}
