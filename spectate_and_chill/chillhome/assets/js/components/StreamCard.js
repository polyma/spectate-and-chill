var React = require('react');
var StreamCard = React.createClass({
    _getChampion: function(championId) {
        var champions = "";
        $.getJSON('http://ddragon.leagueoflegends.com/cdn/6.19.1/data/en_US/champion.json', function(data) {
            champions = JSON.stringify(data);
            var championIcon = "";
            for (var champion in champions['data']) {
                //console.log(champion['key']);
                //console.log(championId);
                if (champion['key'].equals(championId)) {
                    championIcon = "http://ddragon.leagueoflegends.com/cdn/6.19.1/img/champion" + champion['image']['full'];
                    //console.log(championIcon);
                }
                break;
            }
            return {championIcon};
        });
    },

    _getTwitchWidget(e) {
        e.preventDefault();
        this.props._setTwitchVideo(this.state.showTwitchWidget);
    },

    render: function() {
        var champion = this._getChampion(this.props.championId);
        var url = "https://www.twitch.tv/" + this.props.name;
        return (
          <div className="animated">
            {this.props.displayName}
            {this.props.online ?
                // Online card
                <div className="online-card">
                    <div className="card-name">
                        <button onClick={this._getTwitchWidget} type="submit" className="submit-form live-button btn-success"><div className="online"></div>LIVE</button>
                        <a href={this.url} target="_blank" >{this.props.name}</a>
                    </div>
                    <div className="card-pics">
                        <img className="online-pic" src={this.props.logo}></img>
                        <img className="online-pic" src={champion}></img>
                        <span className="lane"> {this.props.lane ? this.props.lane : null} </span>
                    </div>
                    <img className="stream-preview" src={this.props.previewURL_large}></img>
                </div>
            :
                // Offline card
                <div className="offline-card">
                    <div className="card-name">
                        <div className="offline"><p>OFFLINE</p></div>
                        <a href={this.url} target="_blank" >{this.props.name}</a>
                    </div>
                    <img className="offline-pic" src={this.props.logo}></img>
                </div>
            }
          </div>
        );
    }
});

module.exports = StreamCard;
