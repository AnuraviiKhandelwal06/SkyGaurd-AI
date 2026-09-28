
import { useState } from "react";
import { useSearchParams } from "react-router-dom";
import {
  Activity,
  Thermometer,
  Gauge,
  Droplets,
  Wrench,
  CheckCircle
} from "lucide-react";

import { useStationsData, useStationData } from "../hooks/useStationsData";
import { normalizeStatus } from "../utils/statusHelper";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer
} from "recharts";

const sensorIcons = {
  Temperature: Thermometer,
  Pressure: Gauge,
  Humidity: Droplets
};

const statusColors = {
  Healthy: "text-green-600 bg-green-50",
  Warning: "text-yellow-600 bg-yellow-50",
  Faulty: "text-red-600 bg-red-50"
};

function SensorHealth() {
  const [searchParams, setSearchParams] = useSearchParams();

  
  const { data: stations, loading: stationsLoading } = useStationsData();
  const selectedId = searchParams.get("station") || (stations && stations.length > 0 ? stations[0].station_id : "");
  const selectedStation = (stations || []).find((s) => s.station_id === selectedId);
  const { data: stationDetail } = useStationData(selectedId);
  const healthData = stationDetail?.sensor_health;
  
  const chartData = [
      { name: "Jan", health: 100 },
      { name: "Feb", health: 100 },
      { name: "Mar", health: 100 },
      { name: "Apr", health: 95 },
      { name: "May", health: 98 },
      { name: "Jun", health: 92 },
      { name: "Jul", health: 90 },
      { name: "Aug", health: 85 },
      { name: "Sep", health: 88 },
      { name: "Oct", health: 80 },
      { name: "Nov", health: 82 },
      { name: "Dec", health: healthData?.health_score_pct || 100 }
  ];
  
  const sensorsList = healthData ? [
    { type: "Temperature", health: healthData.sensor_breakdown?.temperature_sensor_health_pct || 100, status: (healthData.sensor_breakdown?.temperature_sensor_health_pct||100) >= 80 ? 'Healthy' : 'Faulty' },
    { type: "Pressure", health: healthData.sensor_breakdown?.pressure_sensor_health_pct || 100, status: (healthData.sensor_breakdown?.pressure_sensor_health_pct||100) >= 80 ? 'Healthy' : 'Faulty' },
    { type: "Humidity", health: healthData.sensor_breakdown?.humidity_sensor_health_pct || 100, status: (healthData.sensor_breakdown?.humidity_sensor_health_pct||100) >= 80 ? 'Healthy' : 'Faulty' }
  ] : [];


  const [maintenance, setMaintenance] = useState({});

  function updateMaintenance(sensorType, newStatus) {
    const key = `${selectedId}-${sensorType}`;

    setMaintenance((previous) => ({
      ...previous,
      [key]: newStatus
    }));
  }

  return (
    <div className="p-8 space-y-6">

      <div>
        <h1 className="text-2xl font-bold text-gray-800">
          Sensor Health Monitoring
        </h1>

        <p className="text-gray-500 mt-1">
          Indian AWS Sensor Performance and Maintenance
        </p>

        <p className="text-xs text-amber-700 mt-2">
          Demonstration data — not live sensor diagnostics.
        </p>
      </div>

      {/* Station selection */}
      <div className="bg-white rounded-xl border border-gray-200 p-5">

        <label
          htmlFor="station-select"
          className="block text-sm font-medium text-gray-700 mb-2"
        >
          Select AWS Station
        </label>

        <select
          id="station-select"
          value={selectedId}
          onChange={(e) =>
            setSearchParams({ station: e.target.value })
          }
          className="w-full md:w-96 border border-gray-200 rounded-lg p-3 bg-white cursor-pointer"
        >
          {(stations||[]).map((station) => (
            <option key={station.station_id} value={station.station_id}>
              {station.location} ({station.station_id})
            </option>
          ))}
        </select>

      </div>

      {/* Sensor details */}
      {selectedStation && healthData && (
        <>
          <div className="bg-white rounded-xl border border-gray-200 p-5">

            <div className="flex items-center gap-3">
              <Activity className="text-teal-600" />

              <div><h2 className="text-lg font-semibold">{selectedStation.location}</h2><p className="text-sm text-gray-500">{selectedStation.station_id}</p></div></div><div className="flex gap-8"><div className="text-right"><p className="text-sm text-gray-500 font-medium">Fleet/Station Health</p><p className="text-2xl font-bold">{(healthData?.health_score_pct || 100).toFixed(1)}%</p></div><div className="text-right"><p className="text-sm text-gray-500 font-medium">MTBF / Est RUL</p><p className="text-2xl font-bold">{healthData?.estimated_rul_days || 0} days</p></div></div></div><div className="mb-8"><p className="text-sm text-gray-500 font-medium mb-4 mt-6">Degradation Trend</p><div className="h-[200px] w-full"><ResponsiveContainer width="100%" height="100%"><LineChart data={chartData}><CartesianGrid strokeDasharray="3 3" vertical={false} /><XAxis dataKey="name" axisLine={false} tickLine={false} tick={{fontSize: 12, fill: "#9ca3af"}} /><YAxis domain={[0, 100]} axisLine={false} tickLine={false} tick={{fontSize: 12, fill: "#9ca3af"}} /><Tooltip /><Line type="monotone" dataKey="health" stroke="#0d9488" strokeWidth={2} dot={{r: 3, fill: "#0d9488"}} /></LineChart></ResponsiveContainer></div><div>
            </div>

          </div>

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-5">

            {sensorsList.map((sensor) => {
              const Icon = sensorIcons[sensor.type];
              const key = `${selectedId}-${sensor.type}`;

              const maintenanceStatus =
                maintenance[key] || "Not Scheduled";

              return (
                <div
                  key={sensor.type}
                  className="bg-white rounded-xl border border-gray-200 p-5 shadow-sm"
                >
                  <div className="flex items-center justify-between mb-4">

                    <div className="flex items-center gap-2">
                      <Icon className="text-teal-600" size={22} />

                      <h3 className="font-semibold">
                        {sensor.type} Sensor
                      </h3>
                    </div>

                    <span
                      className={`text-xs px-3 py-1 rounded-full ${
                        statusColors[sensor.status]
                      }`}
                    >
                      {sensor.status}
                    </span>

                  </div>

                  <p className="text-sm text-gray-500">
                    Health Score (Demo)
                  </p>

                  <p className="text-3xl font-bold text-gray-800 mt-1">
                    {sensor.health.toFixed(1)}%
                  </p>

                  <div className="w-full bg-gray-100 rounded-full h-2 mt-4">
                    <div
                      className={`h-2 rounded-full ${
                        normalizeStatus(sensor.status) === "Healthy"
                          ? "bg-green-500"
                          : normalizeStatus(sensor.status) === "Warning"
                          ? "bg-yellow-500"
                          : "bg-red-500"
                      }`}
                      style={{ width: `${sensor.health.toFixed(1)}%` }}
                    />
                  </div>

                  <div className="mt-6 border-t pt-4">

                    <p className="text-sm text-gray-500 mb-3">
                      Maintenance:{" "}
                      <strong>{maintenanceStatus}</strong>
                    </p>

                    {maintenanceStatus === "Not Scheduled" ? (
                      <button
                        type="button"
                        onClick={() =>
                          updateMaintenance(
                            sensor.type,
                            "Scheduled"
                          )
                        }
                        className="flex items-center gap-2 px-4 py-2 bg-teal-600 text-white rounded-lg hover:bg-teal-700 cursor-pointer"
                      >
                        <Wrench size={16} />
                        Schedule Maintenance
                      </button>
                    ) : (
                      <button
                        type="button"
                        onClick={() =>
                          updateMaintenance(
                            sensor.type,
                            "Completed"
                          )
                        }
                        disabled={maintenanceStatus === "Completed"}
                        className="flex items-center gap-2 px-4 py-2 bg-green-600 text-white rounded-lg disabled:opacity-50 disabled:cursor-not-allowed cursor-pointer"
                      >
                        <CheckCircle size={16} />
                        {maintenanceStatus === "Completed"
                          ? "Maintenance Completed"
                          : "Mark as Completed"}
                      </button>
                    )}

                  </div>
                </div>
              );
            })}

          </div>
        </>
      )}

    </div>
  );
}

export default SensorHealth;