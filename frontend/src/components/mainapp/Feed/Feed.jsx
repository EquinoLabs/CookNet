// components/Feed.jsx
import React, { useState, useEffect, useCallback } from 'react';
import PostCard from '../../common/PostCard/PostCard';
import { useInfiniteScroll } from '../../../hooks/UseInfiniteScroll';
import './Feed.scss';
import { getFeedPosts } from '../../../api/actions';

const Feed = () => {
  const [posts, setPosts] = useState([]);
  const [hasMore, setHasMore] = useState(true);
  const [nextCursor, setNextCursor] = useState(null);
  const [initialLoading, setInitialLoading] = useState(true);
  const [error, setError] = useState(null);

  // Fetch posts function
  const fetchPosts = useCallback(async (cursor = null) => {
    try {
      const data = await getFeedPosts(cursor);
      return data;
    } catch (err) {
      setError(err.message);
      return null;
    }
  }, []);

  // Initial load
  useEffect(() => {
    const loadInitialPosts = async () => {
      setInitialLoading(true);
      const data = await fetchPosts();
      console.log("Feed data:", data);
      
      if (data) {
        setPosts(data.posts);
        setHasMore(data.has_more);
        setNextCursor(data.next_cursor);
      }
      
      setInitialLoading(false);
    };

    loadInitialPosts();
  }, [fetchPosts]);

  // Load more posts (for infinite scroll)
  const loadMorePosts = useCallback(async () => {
    if (!hasMore || !nextCursor) return;

    const data = await fetchPosts(nextCursor);
    
    if (data) {
      setPosts(prev => [...prev, ...data.posts]);
      setHasMore(data.has_more);
      setNextCursor(data.next_cursor);
    }
  }, [fetchPosts, hasMore, nextCursor]);

  // Setup infinite scroll
  const { loading: scrollLoading } = useInfiniteScroll(loadMorePosts);

  if (initialLoading) {
    return (
      <div className="feed-loading">
        <div className="loading-spinner">Loading feed...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="feed-error">
        <p>Error loading feed: {error}</p>
        <button onClick={() => window.location.reload()}>Retry</button>
      </div>
    );
  }

  return (
    <div className="feed-container">
      <div className="feed">
        {posts.map((post) => (
          <PostCard key={post.id} post={post} />
        ))}
        
        {scrollLoading && (
          <div className="loading-more">
            <div className="loading-spinner">Loading more posts...</div>
          </div>
        )}
        
        {!hasMore && posts.length > 0 && (
          <div className="end-of-feed">
            <p>You're all caught up! 🎉</p>
          </div>
        )}
        
        {posts.length === 0 && (
          <div className="empty-feed">
            <p>No posts to show. Follow some users to see their recipes!</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default Feed;
