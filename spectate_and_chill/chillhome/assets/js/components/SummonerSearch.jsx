import React from "react"
import {SearchInputForm} from "./SearchInputForm.jsx";

export class SummonerSearch extends React.Component {

    render() {
        return (
            <div className="row">
                <div className="col-xs-12 summ-search">
                    <SearchInputForm />
                </div>
            </div>
        );
    }
}
