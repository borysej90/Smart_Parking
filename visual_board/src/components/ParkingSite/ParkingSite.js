import './ParkingSite.css';
import LotItem from '../LotItem/LotItem';
import React, {useEffect} from 'react';
import YouAreHere from '../YouAreHere/YouAreHere';

function ParkingSite() {
  const [lots, setLots] = React.useState([])

  async function GetData(){
    const response = await fetch(`${process.env.REACT_APP_base_url}/api/sites/${process.env.REACT_APP_parking_site}/lots/`)
    return await response.json()
  } 
  useEffect(() => {
    GetData()
    .then(lots => {
      setLots(lots)
    })
    const interval = setInterval(() => {
      GetData()
      .then(lots => {
        setLots(lots)
      })
    }, 15000);//15 sec
    return () => clearInterval(interval);
  }, []);
      
  return (
        <div className="parkingSite" style={{backgroundImage:`url(${process.env.PUBLIC_URL}/images/parking${process.env.REACT_APP_parking_site}.png`}}>
            {lots.map((lot, idx) => {
                return <LotItem lot={lot}
                            key={idx}
                />
            })}
          <YouAreHere/>
        </div>
);
}
  
export default ParkingSite;