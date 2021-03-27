import './LotItem.css';
import React from "react";
import Img from '../../images/logo_white.png';

export default function LotsItem({lot}) {
  const styles = {  
    marginLeft: lot.position_on_board[0], 
    marginTop: lot.position_on_board[1],
    width: lot.shape_on_board[0],
    height: lot.shape_on_board[1] 
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
          <img className="img_prop" src={Img} alt="for_disabled"/>
        </div>  
      ) : (
        <div id = {lot.id} className={classes.join(' ')} style={styles}></div>  
      )}
    </>
    
  );
}
  
