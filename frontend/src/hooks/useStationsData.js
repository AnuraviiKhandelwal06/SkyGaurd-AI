import { useState, useEffect, useCallback } from 'react';
import { BASE_URL } from '../config/api';

export function useStationsData() {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [lastUpdated, setLastUpdated] = useState(null);

  const fetchData = useCallback(async () => {
    try {
      const response = await fetch(`${BASE_URL}/predict/all`);
      if (!response.ok) {
        throw new Error('Station data unavailable');
      }
      const result = await response.json();
      
      // result might be an array of station diagnosis objects
      setData(Array.isArray(result) ? result : Object.values(result));
      setError(null);
      setLastUpdated(new Date());
    } catch (err) {
      setError(err.message || 'Station data unavailable — check that the ML service is running');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchData();
    let pollMs = 30000;
    try {
      const saved = JSON.parse(localStorage.getItem("skyguard-settings") || "{}");
      if (saved.refreshInterval) {
        pollMs = parseInt(saved.refreshInterval, 10) * 1000;
      }
    } catch(e) {}
    const interval = setInterval(fetchData, pollMs);
    return () => clearInterval(interval);
  }, [fetchData]);

  return { data, loading, error, lastUpdated, refetch: fetchData };
}

export function useStationData(stationId) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!stationId) return;
    
    let isMounted = true;
    const fetchData = async () => {
      setLoading(true);
      try {
        const response = await fetch(`${BASE_URL}/predict?station_id=${stationId}`);
        if (!response.ok) {
          throw new Error('Station data unavailable');
        }
        const result = await response.json();
        if (isMounted) {
          setData(result);
          setError(null);
        }
      } catch (err) {
        if (isMounted) {
          setError(err.message || 'Station data unavailable — check that the ML service is running');
        }
      } finally {
        if (isMounted) {
          setLoading(false);
        }
      }
    };
    
    fetchData();
    return () => { isMounted = false; };
  }, [stationId]);

  return { data, loading, error };
}
