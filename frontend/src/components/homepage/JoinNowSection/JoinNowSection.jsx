import './JoinNowSection.scss'

export default function JoinNowSection() {
    const JoinBtnClicked = () => {
        window.location.href = "/signup";
    }

    return (
        <section className="join-now-section">
          <button onClick={JoinBtnClicked} className="join-btn">
              Join & Share Your Recipes
          </button>
        </section>
    );
}
