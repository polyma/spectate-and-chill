import React from "react"

export class About extends React.Component {
    render() {
        return (
            <div className="row">
              <div className="col-xs-8 col-xs-offset-2 about animated fadeIn">
                <p><span className="purple">INPUT YOUR SUMMONER NAME</span></p>
                <p>WE’LL <span className="purple">ANALYZE YOUR MATCH HISTORY</span> AND USE OUR UNIQUE RECOMMENDATION ALGORITHM TO <span className="purple">LEARN HOW YOU PLAY</span>. ONE TRICK PONY? FOLLOWING THE CURRENT META? STRANGE PICKS FROM BEYOND THE VOID? SPECTATE AND CHILL WILL PINPOINT YOUR PLAYSTYLE.</p>
                <p>DISCOVER TWITCH.TV STREAMERS</p>
                <p>WE FIND THE BEST STREAMERS ON TWITCH.TV WHO MATCH YOUR PLAYSTYLE AND RECOMMEND WHAT TO WATCH. EVERY SUGGESTION IS <span className="purple">CUSTOM-TAILORED</span> TO FIT YOU.</p>
                <p>SPECTATE AND CHILL</p>
                <p>PICK A STREAM AND KICK BACK! IF YOU WANNA <span className="purple">BROADEN YOUR CHAMP POOL</span> IN YOUR FAVORITE LANE, <span className="purple">LEARN HOW TO IMPROVE AT TEEMO</span>, OR SIMPLY BE ENTERTAINED, SPECTATE AND CHILL HAS YOU COVERED!</p>
              </div>
            </div>
        );
    }
}
