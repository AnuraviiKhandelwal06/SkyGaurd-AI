import { useState, useEffect, useCallback } from 'react';
import { BASE_URL } from '../config/api';
import { stations as mockStations } from '../data/mockdata';
import { anomalies as mockAnomalies } from '../data/mockanomalies';
import { sensorHealth as mockSensorHealth } from '../data/mocksensorhealth';

const DATA_MODE = import.meta.env.VITE_DATA_MODE || 'static';

/**
 * Transform mock station data to match the API response shape
 * that all pages (dashboard, livestations, anomalydetection, etc.) expect.
 */
function transformMockStations(stations) {
  return stations.map((s) => {
    const anomaly = mockAnomalies.find((a) => a.stationId === s.id);
    const health = mockSensorHealth.find((h) => h.stationId === s.id);

    return {
      station_id: s.id,
      station_name: s.name,
      location: s.location || s.name,
      latitude: s.latitude,
      longitude: s.longitude,
      status: s.status,
      anomaly_type: anomaly ? anomaly.suspectedFault : null,
      severity_score: anomaly ? anomaly.confidence : null,
      confidence_score: anomaly ? anomaly.confidence : null,
      original_telemetry: {
        temperature_2m: s.temperature,
        relative_humidity_2m: s.humidity,
        surface_pressure: s.pressure,
        pressure_msl: s.pressure,
      },
      diagnosis: anomaly
        ? {
            diagnosis: {
              evidence_chain: anomaly.evidence,
            },
          }
        : null,
      correction: anomaly
        ? {
            id: anomaly.id,
            corrected_value: anomaly.suggestedValue,
          }
        : null,
      explainability: {
        confidence_pct: anomaly ? anomaly.confidence * 100 : 85.0,
      },
      sensor_health: health
        ? {
            health_score_pct: health.sensors.reduce((sum, sen) => sum + sen.health, 0) / health.sensors.length,
            mtbf_days: 120,
            estimated_rul_days: 90,
            sensor_breakdown: {
              temperature_sensor_health_pct: health.sensors.find((x) => x.type === 'Temperature')?.health || 100,
              pressure_sensor_health_pct: health.sensors.find((x) => x.type === 'Pressure')?.health || 100,
              humidity_sensor_health_pct: health.sensors.find((x) => x.type === 'Humidity')?.health || 100,
            },
            degradation_trend: [
              { name: 'Jan', health: 100 },
              { name: 'Feb', health: 99 },
              { name: 'Mar', health: 98 },
              { name: 'Apr', health: 96 },
              { name: 'May', health: 95 },
              { name: 'Jun', health: 93 },
              { name: 'Jul', health: 91 },
              { name: 'Aug', health: 89 },
              { name: 'Sep', health: 87 },
              { name: 'Oct', health: 85 },
              { name: 'Nov', health: 83 },
              {
                name: 'Dec',
                health: health.sensors.reduce((sum, sen) => sum + sen.health, 0) / health.sensors.length,
              },
            ],
          }
        : null,
    };
  });
}

const staticData = transformMockStations(mockStations);

export function useStationsData() {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [lastUpdated, setLastUpdated] = useState(null);

  const fetchData = useCallback(async () => {
    // Static / demo mode — use bundled mock data, no network call
    if (DATA_MODE === 'static') {
      setData(staticData);
      setError(null);
      setLastUpdated(new Date());
      setLoading(false);
      return;
    }

    // Live API mode
    try {
      const response = await fetch(`${BASE_URL}/predict/all`);
      if (!response.ok) {
        throw new Error('Station data unavailable');
      }
      const result = await response.json();
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

    // Only poll when using live API
    if (DATA_MODE === 'static') return;

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

    // Static mode — find station from mock data
    if (DATA_MODE === 'static') {
      const found = staticData.find((s) => s.station_id === stationId);
      setData(found || null);
      setError(found ? null : 'Station not found in demo data');
      setLoading(false);
      return;
    }

    // Live API mode
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
