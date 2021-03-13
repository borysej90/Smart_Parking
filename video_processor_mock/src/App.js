import React, {useEffect, useState} from "react";
import "./App.css";
import Lot from "./components/lot/Lot";


function App() {
    const [lots, setLots] = useState([]);
    const [error, setError] = useState(null);
    const [isLoaded, setIsLoaded] = useState(false);
    useEffect(() => {
        const requestOptions = {
            method: "GET",
            headers: {"Content-Type": "application/json"},
        }
        fetch("http://localhost:8000/api/sites/1/lots/", requestOptions)
            .then(res => res.json())
            .then(
                (result) => {
                    setIsLoaded(true);
                    setLots(result);
                },
                (error) => {
                    setIsLoaded(true);
                    setError(error);
                }
            )
    }, [])

    if (error) {
        return <div>[ERROR]: {error.message}</div>;
    } else if (!isLoaded) {
        return <div>Loading...</div>;
    } else {
        return (
            <div className="App">
                {lots.map(el => <Lot key={el.id} lot={el}/>)}
            </div>
        );
    }
}

export default App;
