// hooks/useInfiniteScroll.js
import { useState, useEffect, useCallback } from 'react';

export const useInfiniteScroll = (fetchMore) => {
  const [loading, setLoading] = useState(false);

  const handleScroll = useCallback(() => {
    if (loading) return;

    // Check if user scrolled near bottom (within 100px)
    if (
      window.innerHeight + document.documentElement.scrollTop + 100 >=
      document.documentElement.offsetHeight
    ) {
      setLoading(true);
      fetchMore().finally(() => setLoading(false));
    }
  }, [fetchMore, loading]);

  useEffect(() => {
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, [handleScroll]);

  return { loading };
};
