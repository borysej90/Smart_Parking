import React, {useState, useEffect} from "react";
import "./Lot.css";


function Lot(props) {
    const [lot, setLot] = useState(props.lot)



    function occupy(id) {

        setLot({...lot, is_occupied: true})
    }

    return (
        <div className="lot-container-s">
            {
                lot.parking_side_id % 6 === 0 ?
                    <div className="lot-container-s">
                        {lot.parking_side_id !== 6 ? <div className="hr"/> : null}
                        <button onClick={() => occupy(lot.id)} disabled={lot.is_occupied}
                                className={lot.is_occupied ? "lot lot-occupied" : "lot"}
                                key={lot.id}>{lot.parking_side_id}</button>
                    </div>
                    :
                    <div className="lot-container">
                        <button onClick={() => occupy(lot.id)} disabled={lot.is_occupied}
                                className={lot.is_occupied ? "lot lot-occupied" : "lot"}
                                key={lot.id}>{lot.parking_side_id}</button>
                    </div>
            }
        </div>
    );
}

export default Lot;
