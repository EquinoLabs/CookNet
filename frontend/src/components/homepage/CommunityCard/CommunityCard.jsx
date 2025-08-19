import './CommunityCard.scss'

export default function CommunityCard({ name, icon: Icon }) {
  return (
    <div className="community-card">
      <Icon className="community-icon" size={40} color="#4F9B3EFF" />
      <h3 className="community-name">{name}</h3>
    </div>
  );
}
