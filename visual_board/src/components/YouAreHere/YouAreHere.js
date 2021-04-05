import './YouAreHere.css';
function YouAreHere() {
  return (
    <div className="youHere">
        <img className="imgProp" src={process.env.PUBLIC_URL + "/images/you_are_here.png"} alt="YouHere"/>
    </div>
  );
}

export default YouAreHere;
