import React, {useState, useEffect} from "react";
import "./Lot.css";


function Lot(props) {
    const [lot, setLot] = useState(props.lot)


    function occupy() {
        const requestOptions = {
            method: "PUT",
            headers: {'Content-Type': 'application/json;charset=UTF-8'},
            body: JSON.stringify({...lot, is_occupied: !lot.is_occupied}),
        };
        fetch(`http://localhost:8000/api/sites/1/lots/${lot.id}/`, requestOptions)
            .then(response => {
                const data = response.json();
                if (!response.ok) {
                    const error = (data && data.message) || response.status;
                    return Promise.reject(error);
                }
                setLot({...lot, is_occupied: !lot.is_occupied})
            })
            .catch(error => {
                console.error("There was an error!", error);
            });
    }

    return (
        <div className="lot-container-s">
            {
                lot.id % 6 === 0 ?
                    <div className="lot-container-s">
                        {lot.id !== 6 ? <div className="hr"/> : null}
                        <button onClick={() => occupy()} className={lot.is_occupied ? "lot lot-occupied" : "lot"}
                                key={lot.id}>{lot.id}</button>
                    </div>
                    :
                    <div className="lot-container">
                        <button onClick={() => occupy()} className={lot.is_occupied ? "lot lot-occupied" : "lot"}
                                key={lot.id}>{lot.id}</button>
                    </div>
            }
        </div>
    );
}

export default Lot;
