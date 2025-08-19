import CommunityCard from "../CommunityCard/CommunityCard";
import './CommunitiesSection.scss';

export default function CommunitiesSection({ communities }) {
  return (
    <section className="communities-section">
      <h2 className="section-title">Explore Communities</h2>
      <div className="communities-grid">
        {communities.map((community, index) => (
          <CommunityCard key={index} {...community} />
        ))}
      </div>
    </section>
  );
}
