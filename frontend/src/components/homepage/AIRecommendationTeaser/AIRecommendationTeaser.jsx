import './AIRecommendationTeaser.scss';

export default function AIRecommendationTeaser() {
    const TryAIBtnClicked = () => {
        window.location.href = "/ai-features";
    }

  return (
    <section className="AI-Recommendation-Teaser">
        <div className="container">
            <div className="content">
                <h2 className="title">Unlock Your Culinary Potential with AI</h2>
                <p className="description">
                    AI-powered recipe suggestions based on your mood or what’s in your fridge. Get personalized recipe suggestions, ingredient pairing ideas, and cooking tips powered by advanced AI. Discover new favorites effortlessly.
                </p>
            </div>
            <button onClick={TryAIBtnClicked} className="try-ai-btn">
                Try AI Recommendations
            </button>
        </div>
    </section>
  );
}
