import { useState } from "react";
import IconButton from "@mui/material/IconButton";
import SearchIcon from "@mui/icons-material/Search";
import './searchBar.css';

export function AiSearchBar({setAskedQuery}) {
    const [searchQuery, setSearchQuery] = useState("");

    const filterData = (query, data) => {
        console.log(query,data);
        if (query.length===0) {
            return data;
        } else {
            return data.filter((d) => d.toLowerCase().includes(query.toLowerCase()));
        }
    };
    const data = [
        "Paris",
        "London",
        "New York",
        "Tokyo",
        "Berlin",
        "Buenos Aires",
        "Cairo",
        "Canberra",
        "Rio de Janeiro",
        "Dublin"
    ];

    function handleSubmit(event){
        console.log(event);
        event.preventDefault();
        console.log(searchQuery);
        setAskedQuery(searchQuery);
    }

    const dataFiltered = filterData(searchQuery, data);

    return (
        <div style={{"display" : "flex", "justifyContent": "center", "alignItems" : "start", "marginTop": "4.5rem"}}>
            <img src="/describe-outfit.svg" style={{"width" : "15vw"}}/>
            <div className="search-wrapper" >
            <div>
            <form onSubmit={handleSubmit}>
                <IconButton type="submit" aria-label="search">
                    <SearchIcon style={{ fill: "black", fontSize: "1.5rem", margin: "0px" }} />
                </IconButton>
                <input type="text" className="text-field" autoFocus value={searchQuery} onInput={e => setSearchQuery(e.target.value)}/>
            </form>
            </div>
            <div style={{"height" : "1px","opacity" : "0.2", "backgroundColor" : "black","margin" : "0.5rem 0rem"}}></div>
            <div style={{ padding: 3 }}>
                {dataFiltered.map((d) => (
                    <div className="filtered-text" key={d.id}>
                        {d}
                    </div>
                ))}
            </div>
        </div>
        </div>
    );
}