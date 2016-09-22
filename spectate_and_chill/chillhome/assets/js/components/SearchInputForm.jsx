import React from "react"

export class SearchInputForm extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            summonerName: '',
            region: 'euw',
        }
        this.changeName = this._changeName.bind(this)
        this.changeRegion = this._changeRegion.bind(this);
        this.validateInput = this._validateInput.bind(this);
        // this.getSummonerData = this._getSummonerData.bind(this);
    }

    _validateInput(e) {
        e.preventDefault();
        var re = new RegExp("^([\p{L}_. ]+)$");
        if (re.test(summonerName)) {

        }
    }

     render() {
        return (
            <div className="inputForm form-horizontal">
                <div className="form-group row">
                <form onSubmit={this.validateInput}>
                    <div className="col-xs-6 col-xs-offset-2 ">
                        <input value={this.state.summonerName} onChange={this.changeName} id="summoner" className="form-control search-bar" placeholder="Summoner name" ></input>
                    </div>
                    <div>
                        <select className="col-xs-2 form-control region-btn" value={this.state.region} onChange={this.changeRegion}>
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
                    <button type="submit" className="submit-button"><span className="glyphicon glyphicon-search"></span></button>
                    </div>
                    </form>
                </div>
            </div>
        );
    }

    _changeName(e) {
        this.setState({summonerName: e.value});
    }

    _changeRegion(e) {
        this.setState({region: e.value});
    }
}
