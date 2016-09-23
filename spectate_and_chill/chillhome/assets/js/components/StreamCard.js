var React = require('react');
var StreamCard = React.createClass({
  render: function() {
    return (
      <div className="animated">
        {this.props.displayName}
        {this.props.online
          ? "IS ONLINE!!!!"
        : null}
      </div>
    );
  },
});

module.exports = StreamCard;
