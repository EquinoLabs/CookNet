import './FeaturedCreators.scss'

export default function FeaturedCreators({ creators }) {
  return (
    <section className="featured-creators">
      <h2 className="featured-creators-title">Top Creators</h2>
      <div className="creators-grid">
        {creators.map((creator, i) => (
          <div key={i} className="creator-card">
            <img
              src={creator.avatar}
              alt={creator.name}
              className="creator-avatar"
            />
            <h3 className="creator-name">{creator.name}</h3>
            <span className="creator-signature-dish">{creator.signature}</span>
          </div>
        ))}
      </div>
    </section>
  );
}
