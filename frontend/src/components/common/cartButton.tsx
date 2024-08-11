import React from "react";
import ShoppingCartIcon from "@mui/icons-material/ShoppingCart";
import "./cartButton.css";

type CartButtonProps = {
  CartDisabled?: boolean;
  handleClick?: () => void;
};

export function CartButton<CartButtonProps>({ CartDisabled = false, handleClick }) {
  return (
    <button className="cart-button" disabled={CartDisabled} onClick={handleClick}>
      <ShoppingCartIcon sx={{ paddingRight: "0.25rem" }} />
      <div className="cart-button-text">Cart</div>
    </button>
  );
}
