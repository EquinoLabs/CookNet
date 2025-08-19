export default function RecipeCard({ recipe, onClick }) {
  return (
    <div
      onClick={() => onClick(recipe)}
      className="border rounded-lg p-4 cursor-pointer hover:shadow-lg"
    >
      <img
        src={recipe.image}
        alt={recipe.title}
        className="w-full h-40 object-cover rounded"
      />
      <h3 className="mt-2 font-semibold">{recipe.name}</h3>
    </div>
  );
}
