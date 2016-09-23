import React from "react"

export class SummonerSearch extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            summonerName: '',
            region: 'na',
            error: null
        }
        this.changeName = this._changeName.bind(this)
        this.changeRegion = this._changeRegion.bind(this);
        this.validateInput = this._validateInput.bind(this);
        // this.getSummonerData = this._getSummonerData.bind(this);
    }

    _validateInput(e) {
        e.preventDefault();
        this.props.getSummonerData(this.state.summonerName, this.state.region);
        this.state.summonerName = this.state.summonerName.trim();
        this.state.summonerName = this.state.summonerName.toLowerCase();
        //var re = new RegExp("/[,.\s]+/g");
        //if (re.test(this.state.summonerName)) {
        //    this.setState({error: 'INVALID SUMMONER NAME'})
        //} else {
        //    console.log('valid input!');
        this.props.getSummonerData(this.state.summonerName, this.state.region);
    }

    render() {
        return (
            <div className="row">
              <div className="inputForm form-horizontal animated fadeInDown col-xs-8 col-xs-offset-2">
                <div className="form-group ">
                  {this.state.error
                    ? console.log("error")
                  : null}
                  <form >
                    <div className="row summ-search">
                      <div className="col-xs-9">
                        <input value={this.state.summonerName} onChange={this.changeName} id="summoner" className="form-control search-form" placeholder="Summoner name"></input>
                      </div>
                      <div className="col-xs-2 region-btn">
                        <select className="form-control region-form" value={this.state.region} onChange={this._changeRegion}>
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
                      <div className="col-xs-1 submit submit-button">
                        <button onClick={this.validateInput} type="submit" className="submit-form">
                                        <span className="glyphicon glyphicon-search"></span>
                                    </button>
                                </div>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        );
    }

    _changeName(e) {
        this.setState({summonerName: e.target.value});
    }

    _changeRegion(e) {
        this.setState({region: e.target.value});
    }
}
