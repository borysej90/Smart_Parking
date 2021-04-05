import './LotItem.css';
import React from "react";

export default function LotItem({lot}) {
  const styles = {  
    marginLeft: lot.position_on_board[0] / 10 + "%", 
    marginTop: lot.position_on_board[1] / 10 + "vh",
    height: lot.shape_on_board[1] / 10 + "%",
    width: lot.shape_on_board[0] / 10 + "%",
  }
  
  const classes = ["lot"];
  if(lot.is_occupied){
    classes.push("red")
  }
  else{
    classes.push("green")
  }

  return (
    
    <>
      {lot.is_for_disabled ? (
        <div id = {lot.id} className={classes.join(' ')} style={styles}>
          <img className="img_prop" src={process.env.PUBLIC_URL + '/images/logo_white.png'} alt="for_disabled"/>
        </div>  
      ) : (
        <div id = {lot.id} className={classes.join(' ')} style={styles}></div>  
      )}
    </>
    
  );
}
  
