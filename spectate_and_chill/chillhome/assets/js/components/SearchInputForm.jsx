import React from "react"

export class SearchInputForm extends React.Component {
    // _getSummonerData() {
    //     var summonerName = $("#summoner").val();
    //     var region = $("#region").val();
    //     var apiKey = "1d08e678-90be-4c52-b94e-069619ad0e87";
    //
    //     $.ajax({
    //         url: "https://" + region + ".api.pvp.net/api/lol/" + region "/v2.2/matchlist/by-summoner/" + summonerID + "?rankedQueues=RANKED_SOLO_5x5&seasons=SEASON2016&api_key=" + apiKey;
    //         type: 'GET',
    //         dataType: 'json',
    //         data: {},
    //         success: function(json) {
    //             var summonerName = summonerName.replace(" ", "");
    //             var summonerName = summonerName.toLowerCase().trim();
    //             var summonerID = json[summonerName].id;
    //         },
    //         error: function(XMLHttpRequest, textStatus, errorThrown) {
    //             alert("The Summoner does not exist.");
    //         }
    //     });
    //     alert(summonerID);
    // }

    constructor(props) {
        super(props);
        this.state = {
            summonerName: 'insert',
            region: 'euw',
        }
        this.changeName = this._changeName.bind(this)
        this.changeRegion = this._changeRegion.bind(this);
        this.validateInput = this._validateInput.bind(this);
        // this.getSummonerData = this._getSummonerData.bind(this);
    }

    _validateInput(e) {
        e.preventDefault();
        //if everythins is ok
        this.getSummonerData();
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
                        <select className="form-control region-btn" value={this.state.region} onChange={this.changeRegion}>
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
                    <button type="submit"/>
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
