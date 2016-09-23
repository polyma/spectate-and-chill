var React = require('react');
var StreamCard = React.createClass({
    getChampion: function(championId) {
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

    render: function() {
        var champion = this.getChampion(this.props.championId);
        return (
          <div className="animated">
            {this.props.displayName}
            {this.props.online ?
                // Online card
                <div className="online-card">
                    <div className="card-name">
                        <div className="online"><p>ONLINE</p></div>
                        <p>{this.props.name}</p>
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
                        <p>{this.props.name}</p>
                    </div>
                    <img className="offline-pic" src={this.props.logo}></img>
                </div>
            }
          </div>
        );
    }
});

module.exports = StreamCard;
