import React from "react"
import {SearchInputForm} from "./SearchInputForm.jsx";

export class SummonerSearch extends React.Component {

    render() {
        return (
            <div className="row">
                <div className="championSearch">
                    <SearchInputForm/>
                </div>
            </div>
        );
    }
}
