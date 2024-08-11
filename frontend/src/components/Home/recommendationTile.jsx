import { useEffect, useState } from "react";
import { CircularProgress } from "@mui/material";
import { Link } from 'react-router-dom';

import axios from "axios";
import './recommendationTile.css';

function ItemTile({ product_link, product_name, product_price, image_link }) {
    return <div>
        <div class="relative flex w-44 flex-col rounded-xl bg-white bg-clip-border text-gray-700 shadow-md">
            <div class="relative mx-2 mt-2 h-44 overflow-hidden rounded-xl bg-white bg-clip-border text-gray-700 ">
                <img src={image_link} alt="profile-picture" />
            </div>
            <div class="p-2 text-center">
                <h4 class="mb-2 block h-24 font-sans text-md font-semibold leading-snug tracking-normal text-blue-gray-900 antialiased overflow-hidden text-ellipsis">
                    {product_name}
                </h4>
                <p class="block text-black bg-clip-text font-sans text-base font-medium leading-relaxed antialiased">
                    Price: {product_price}
                </p>
            </div>
            <div class="flex justify-center gap-7 p-6 pt-2">
                <a href={product_link}><button>Buy Now</button></a>
            </div>
        </div>
    </div>;
}

export function RecommendationTile({ recommendationsList }) {

    return <div style={{ "display": "flex", "justifyContent": "center" }}>
        {
            <div className="response-tile-wrapper">
                <div className="flex flex-col bg-gray-400 w-full p-4">
                    <div className="tile-text">
                        Here's your recommended outfit
                    </div>
                    <div className="flex flex-row gap-4 mt-4 flex-wrap">

                        {
                            recommendationsList.map((product, idx) => <ItemTile {...product} />)
                        }
                    </div>
                </div>

            </div>
        }
    </div>;
}