// components/PostCard.jsx
import React, { useState } from 'react';
import { Heart, MessageCircle, Share2, Bookmark } from 'lucide-react';
import './PostCard.scss';
import { postLike } from '../../../api/actions';

const PostCard = ({ post, onLike }) => {
  const [liked, setLiked] = useState(false);
  const [likesCount, setLikesCount] = useState(post.likes_count);

  const handleLike = async () => {
    try {
      const data = await postLike(post.id);
      
      setLiked(data.liked);
      setLikesCount(data.likes_count);
    } catch (error) {
      console.error('Failed to like post:', error);
    }
  };

  const formatTimeAgo = (dateString) => {
    const now = new Date();
    const postDate = new Date(dateString);
    const diffInMinutes = Math.floor((now - postDate) / (1000 * 60));
    
    if (diffInMinutes < 60) return `${diffInMinutes}m`;
    if (diffInMinutes < 1440) return `${Math.floor(diffInMinutes / 60)}h`;
    return `${Math.floor(diffInMinutes / 1440)}d`;
  };

  return (
    <div className="post-card">
      {/* Post Header */}
      <div className="post-header">
        <div className="user-info">
          <img 
            src={post.author.avatar_url || '/default-avatar.png'} 
            alt={post.author.username}
            className="avatar"
          />
          <div>
            <h4 className="username">{post.author.username}</h4>
            <span className="time-ago">{formatTimeAgo(post.created_at)}</span>
          </div>
        </div>
        <button className="options-btn">⋯</button>
      </div>

      {/* Recipe Title */}
      {post.recipe_title && (
        <div className="recipe-header">
          <h3 className="recipe-title">{post.recipe_title}</h3>
          {post.cooking_time && (
            <span className="cooking-time">🕐 {post.cooking_time} min</span>
          )}
          {post.difficulty && (
            <span className={`difficulty ${post.difficulty}`}>
              {post.difficulty}
            </span>
          )}
        </div>
      )}

      {/* Post Content */}
      {post.content && (
        <p className="post-content">{post.content}</p>
      )}

      {/* Media */}
      {post.image_url && (
        <div className="post-media">
          <img src={post.image_url} alt="Recipe" className="post-image" />
        </div>
      )}

      {post.video_url && (
        <div className="post-media">
          <video controls className="post-video">
            <source src={post.video_url} type="video/mp4" />
          </video>
        </div>
      )}

      {/* Recipe Details */}
      {(post.ingredients || post.instructions) && (
        <div className="recipe-details">
          {post.ingredients && (
            <div className="ingredients">
              <h4>Ingredients:</h4>
              <p>{post.ingredients}</p>
            </div>
          )}
          {post.instructions && (
            <div className="instructions">
              <h4>Instructions:</h4>
              <p>{post.instructions}</p>
            </div>
          )}
        </div>
      )}

      {/* Post Actions */}
      <div className="post-actions">
        <button 
          className={`action-btn ${liked ? 'liked' : ''}`}
          onClick={handleLike}
        >
          <Heart className={liked ? 'filled' : ''} size={24} />
        </button>
        <button className="action-btn">
          <MessageCircle size={24} />
        </button>
        <button className="action-btn">
          <Share2 size={24} />
        </button>
        <button className="action-btn bookmark">
          <Bookmark size={24} />
        </button>
      </div>

      {/* Post Stats */}
      <div className="post-stats">
        <span className="likes">{likesCount} likes</span>
        {post.comments_count > 0 && (
          <span className="comments">View all {post.comments_count} comments</span>
        )}
      </div>
    </div>
  );
};

export default PostCard;
