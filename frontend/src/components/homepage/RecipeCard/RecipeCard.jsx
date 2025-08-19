import './RecipeCard.scss';

export default function RecipeCard({ title, image, tags, time, votes }) {
  return (
    <div className="recipe-card">
      <img src={image} alt={title} />
      <div className="card-content">
        <h3>{title}</h3>
        <div className="tags">
          {tags?.map((tag, i) => (
            <span key={i} className="tag">
              {tag}
            </span>
          ))}
        </div>
        <div className="info">
          <span>⏱ {time} min</span>
          <span>👍 {votes}</span>
        </div>
      </div>
    </div>
  );
}
