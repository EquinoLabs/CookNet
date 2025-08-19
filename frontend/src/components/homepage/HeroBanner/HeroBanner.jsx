import SearchBar from "../../common/SearchBar/SearchBar";
import './HeroBanner.scss'


export default function HeroBanner() {
    const JoinBtnClicked = () => {
        window.location.href = "/register";
    }

    return (
        <section className="hero-banner">
            <div className="overlay"></div>
            <div className="content">
                <h1>Your cooking community, your recipes, your style</h1>
                <p>Tailored for your taste, mood, and lifestyle</p>
                <SearchBar placeholder="Search recipes, moods, or ingredients…" />
                <button onClick={JoinBtnClicked} className="join-btn">
                    Join & Share Your Recipes
                </button>
            </div>
        </section>
    );
}
