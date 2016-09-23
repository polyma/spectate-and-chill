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
            this.setState({error: 'INVALID SUMMONER NAME'})
        }
    }

    render() {
        return (
            <div className="row">
                <div className="inputForm form-horizontal animated fadeInDown">
                    <div className="form-group col-xs-12">
                        {this.state.error
                        ? <h2>ERROR {this.state.error}</h2>
                        : null}
                        <form onSubmit={this.validateInput}>
                            <div className="search-bar">
                                <input value={this.state.summonerName} onChange={this.changeName} id="summoner" className="form-control search-form" placeholder="Summoner name" ></input>
                            </div>
                            <div className="region-btn">
                                <select className="form-control region-form" value={this.state.region} onChange={this._changeRegion} >
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
                            <div className="submit submit-button">
                                <button type="submit" className="submit-form"><span className="glyphicon glyphicon-search"></span></button>
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
        this.setState({region: e.value});
    }
}
