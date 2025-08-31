import { useState, useEffect } from "react";
import SearchBar from "../../common/SearchBar/SearchBar";
import { getMediaURL } from "../../../api/actions";
import constants from "../../../constants";
import './HeroBanner.scss'


export default function HeroBanner() {
    const [bgUrl, setBgUrl] = useState(null);

    useEffect(() => {
        // fetch only if no url is set yet
        if (!bgUrl) {
            getMediaURL(constants.HomePage.Banner.imageId)
                .then((url) => setBgUrl(url))
                .catch((err) => {
                    console.error("Failed to load banner image:", err);
                });
            console.log("URL", bgUrl)
        }
    }, [bgUrl]);

    const JoinBtnClicked = () => {
        window.location.href = "/register";
    }

    return (
        <section 
            style={{
                background: `url(${bgUrl}) center -100px / cover no-repeat`
            }}
            className="hero-banner"
        >
            <div className="overlay"></div>
            <div className="content">
                <h1>Your cooking community, your recipes, your style</h1>
                <p>Tailored for your taste, mood, and lifestyle</p>
                <SearchBar placeholder={constants.HomePage.Banner.searchbarPlaceholder} />
                <button onClick={JoinBtnClicked} className="join-btn">
                    Join & Share Your Recipes
                </button>
            </div>
        </section>
    );
}
