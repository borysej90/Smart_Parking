import React, {useEffect, useState} from "react";
import "./App.css";
import Lot from "./components/lot/Lot";


function App() {
    const [lots, setLots] = useState([
        {
            id: 1,
            parking_side_id: 1,
            is_occupied: false
        },
        {
            id: 2,
            parking_side_id: 2,
            is_occupied: false
        },
        {
            id: 3,
            parking_side_id: 3,
            is_occupied: false
        },
        {
            id: 4,
            parking_side_id: 4,
            is_occupied: true
        },
        {
            id: 5,
            parking_side_id: 5,
            is_occupied: false
        },
        {
            id: 6,
            parking_side_id: 6,
            is_occupied: false
        },
        {
            id: 7,
            parking_side_id: 7,
            is_occupied: true
        },
        {
            id: 8,
            parking_side_id: 8,
            is_occupied: false
        },
        {
            id: 9,
            parking_side_id: 9,
            is_occupied: false
        },
        {
            id: 10,
            parking_side_id: 10,
            is_occupied: false
        },
        {
            id: 11,
            parking_side_id: 11,
            is_occupied: false
        },
        {
            id: 12,
            parking_side_id: 12,
            is_occupied: false
        }
    ])

    return (
        <div className="App">
            {lots.map(el => <Lot key={el.id} lot={el}/>)}
        </div>
    );
}

export default App;
