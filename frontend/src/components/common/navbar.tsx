import styled from "styled-components";
import React from "react";
import { CartButton } from "./cartButton";
import { PiLink } from "react-icons/pi";
import ShoppingCartIcon from "@mui/icons-material/ShoppingCart";
import { AiFillCaretUp, AiOutlineClose } from "react-icons/ai";
import { Box, ClickAwayListener } from "@mui/material";
import { SxProps } from "@mui/system";
import "./navbar.css";

type NavbarProps = {
  CartDisabled?: Boolean;
  cartItems?: any[];
  setCartItems?: React.Dispatch<React.SetStateAction<any[]>>;
};

type itemProps = {
  product_link: string;
  image_link: string;
  product_price: string;
};

export function Navbar<NavbarProps>({
  CartDisabled = false,
  cartItems = [],
  setCartItems,
}) {
  const [open, setOpen] = React.useState(false);
  const handleClick = () => {
    setOpen((prev) => !prev);
  };

  const handleClickAway = () => {
    setOpen(false);
  };

  const styles: SxProps = {
    position: "absolute",
    top: 28,
    right: 0,
    left: 0,
    zIndex: 1,
    border: "1px solid",
    p: 1,
    bgcolor: "background.paper",
  };

  const testArr = [
    {
      search_query: "Traditional Sherwani",
      product_link:
        "https://www.flipkart.com/brand-boy-self-design-sherwani/p/itm40b5fe68877b3?pid=SRWGHTG9CX8ZNPY9&lid=LSTSRWGHTG9CX8ZNPY99UOAS9&marketplace=FLIPKART&q=Traditional+Sherwani&store=clo%2Fcfv%2Fdra%2Fbrt&srno=s_1_3&otracker=search&iid=9503e3e1-b34c-452a-b5a2-f09560626dc5.SRWGHTG9CX8ZNPY9.SEARCH&ssid=uh4oa5vln40000001692442058484&qH=9f5d829559ced38a",
      product_name: "Brand Boy Self Design Sherwani",
      product_price: "₹1,665",
      image_link:
        "https://rukminim2.flixcart.com/image/612/612/xif0q/sherwani/w/0/6/m-rj-78-brand-boy-original-imaghtg9yxuzps5v.jpeg?q=70",
    },
    {
      search_query: "Mojari",
      product_link:
        "https://www.flipkart.com/aadi-synthetic-leather-lightweight-comfort-summer-trendy-walking-outdoor-daily-use-mojaris-men/p/itm85a853c69e939?pid=SHOFPXYFUWTKAN2G&lid=LSTSHOFPXYFUWTKAN2G4QTCTA&marketplace=FLIPKART&q=Mojari&store=osp&srno=s_1_3&otracker=search&fm=organic&iid=5ba45b1c-398d-4f88-9984-c6268fa49664.SHOFPXYFUWTKAN2G.SEARCH&ppt=sp&ppn=sp&ssid=i0y7zjvats0000001692442062387&qH=2fdf959a4da06988",
      product_name:
        "Synthetic Leather |Lightweight|Comfort|Summer|Trendy|Wa...",
      product_price: "₹482",
      image_link:
        "https://rukminim2.flixcart.com/image/612/612/xif0q/shoe/v/p/m/n1400-9-suson-black-original-imafsfpwqmgqqqsz-bb.jpeg?q=70",
    },
    {
      search_query: "Jodhpuri Pants",
      product_link:
        "https://www.flipkart.com/z-g-trends-2-piece-jodhpuri-blazer-trouser-solid-boys-suit/p/itmacb3085ede70d?pid=SUIFNHB8MZZF8EKW&lid=LSTSUIFNHB8MZZF8EKWCW44DS&marketplace=FLIPKART&q=Jodhpuri+Pants&store=clo&srno=s_1_1&otracker=search&fm=organic&iid=bec0b9f8-17e3-465d-95f7-d0bde7baba85.SUIFNHB8MZZF8EKW.SEARCH&ppt=sp&ppn=sp&ssid=ltal2p6bls0000001692442066460&qH=50efc08c0d52eddf",
      product_name: "Boys 2 Piece Jodhpuri Blazer and Trouser Solid Suit",
      product_price: "₹2,199",
      image_link:
        "https://rukminim2.flixcart.com/image/612/612/xif0q/suit/g/g/z/7-8-years-jp01-z-g-trends-original-imafnhgxbm8dh8s9-bb.jpeg?q=70",
    },
    {
      search_query: "Silk Kurta",
      product_link:
        "https://www.flipkart.com/dap-silk-mills-women-woven-design-straight-kurta/p/itm0ff2821c7a8a9?pid=KTAGNZ95CFTCWRT7&lid=LSTKTAGNZ95CFTCWRT7FQWF9F&marketplace=FLIPKART&q=Silk+Kurta&store=clo%2Fcfv&srno=s_1_3&otracker=search&fm=organic&iid=8cd4b83e-7e3f-45ef-ad14-d017eaaa667a.KTAGNZ95CFTCWRT7.SEARCH&ppt=sp&ppn=sp&ssid=4j5o9z79f40000001692442069618&qH=ee0ca7e897771584",
      product_name: "Women Woven Design Silk Blend Straight Kurta",
      product_price: "₹307",
      image_link:
        "https://rukminim2.flixcart.com/image/612/612/xif0q/kurta/4/z/b/xl-1053-pmshk-original-imagnm7fn9mgggah.jpeg?q=70",
    },
    {
      search_query: "Brocade Nehru Jacket",
      product_link:
        "https://www.flipkart.com/js-collection-sleeveless-floral-print-men-jacket/p/itm184c255148903?pid=JCKGKH6SYQHDUTAU&lid=LSTJCKGKH6SYQHDUTAUGVFFGN&marketplace=FLIPKART&q=Brocade+Nehru+Jacket&store=clo%2Fqvw%2Fz0g%2Fjbm&srno=s_1_3&otracker=search&fm=organic&iid=d08c3384-c6a2-4a0c-b85c-6b4bcf7ad313.JCKGKH6SYQHDUTAU.SEARCH&ppt=sp&ppn=sp&ssid=mt76u7o1cw0000001692442073155&qH=f3fe06577ac5992c",
      product_name: "Men Floral Print Nehru Jacket",
      product_price: "₹1,749",
      image_link:
        "https://rukminim2.flixcart.com/image/612/612/k4rcmfk0/jacket/j/j/f/s-nj-br-blackgolden-treemoda-original-imafnhg3rc7gmjax.jpeg?q=70",
    },
  ];

  return (
    <div className="navbar">
      <div className="navbar-logo">ShopAI</div>
      <ClickAwayListener onClickAway={handleClickAway}>
        <>
          <CartButton CartDisabled={CartDisabled} handleClick={handleClick} />
          {open ? (
            <ItemListWrapper>
              <AiFillCaretUp
                style={{
                  position: "absolute",
                  top: "-0.6rem",
                  right: "0.5rem",
                }}
                color="#fff"
              />
              <div style={{ display: "flex", gap: "1rem" }}>
                {cartItems.length > 0 ? (
                  cartItems.map((item: itemProps) => (
                    <div>
                      <div
                        style={{
                          background: `url(${item.image_link}) no-repeat center center`,
                          backgroundSize: "cover",
                          width: "120px",
                          height: "120px",
                          borderRadius: "6px 6px 0 0",
                        }}
                      >
                        <div
                          style={{
                            display: "flex",
                            flexDirection: "row-reverse",
                          }}
                        >
                          <button
                            style={{
                              backgroundColor: "#C86C53",
                              padding: "4px",
                              borderRadius: "6px",
                            }}
                            onClick={() =>
                              setCartItems(
                                cartItems.filter(
                                  (rec: itemProps) => rec !== item
                                )
                              )
                            }
                          >
                            <AiOutlineClose color="white" />
                          </button>
                        </div>
                        {/* <p>{rec.product_link}</p> */}
                      </div>
                      <div style={{ display: "flex" }}>
                        <div
                          style={{
                            flex: 1,
                            background: "#5F5CD5",
                            display: "flex",
                            justifyContent: "center",
                            alignItems: "center",
                            borderRadius: "0 0 0 6px",
                            color: "#fff",
                            padding: "4px",
                          }}
                        >
                          <p>{item.product_price}</p>
                        </div>

                        <button
                          style={{
                            background: "#fff",
                            display: "flex",
                            justifyContent: "center",
                            alignItems: "center",
                            padding: "4px",
                            borderRadius: "0 0 6px 0",
                          }}
                          onClick={() => window.open(item.product_link, "_blank")}
                        >
                          <ShoppingCartIcon />
                        </button>
                      </div>
                    </div>
                  ))
                ) : (
                  <div className="item">No Items in Cart</div>
                )}
              </div>
            </ItemListWrapper>
          ) : null}
        </>
      </ClickAwayListener>
    </div>
  );
}

const ItemListWrapper = styled.div`
  position: absolute;
  right: 1rem;
  top: 5rem;
  padding: 1rem;
  background: #d9d9d9;
  border-radius: 6px;
`;
