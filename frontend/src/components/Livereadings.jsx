import React, { useState, useEffect } from "react";
import { Thermometer, Gauge, Droplets } from "lucide-react";

function LiveReadings({ stationsData }) {
  const safeStations = stationsData || [];
  
  const [selectedId, setSelectedId] = useState("");

  useEffect(() => {
    if (!selectedId && safeStations.length > 0) {
      try {
        const saved = JSON.parse(
          localStorage.getItem("skyguard-settings") || "{}"
        );
        const exists = safeStations.some(
          (s) => s.station_id === saved.defaultStation
        );
        setSelectedId(exists ? saved.defaultStation : safeStations[0].station_id);
      } catch {
        setSelectedId(safeStations[0].station_id);
      }
    }
  }, [safeStations, selectedId]);

  const selectedStation = safeStations.find(
    (s) => s.station_id === selectedId
  );

  return (
    <div className="bg-white rounded-xl border border-gray-200 shadow-sm p-6 h-full flex flex-col">
      <div className="mb-5">
        <h2 className="text-lg font-bold text-gray-800">
          Live Readings
        </h2>
        <p className="text-sm text-gray-500 mt-1">
          Select an Indian AWS station
        </p>
      </div>

      <select
        value={selectedId}
        onChange={(e) => setSelectedId(e.target.value)}
        className="w-full border border-gray-300 rounded-lg p-3 mb-6 bg-white cursor-pointer focus:outline-none focus:border-teal-500 focus:ring-1 focus:ring-teal-500"
      >
        {safeStations.map((station) => (
          <option key={station.station_id} value={station.station_id}>
            {station.location}
          </option>
        ))}
      </select>

      {selectedStation && (
        <div className="space-y-4 flex-1">
          <div className="flex items-center justify-between bg-orange-50 p-4 rounded-lg border border-orange-100">
            <div className="flex items-center gap-3">
              <Thermometer className="text-orange-500" />
              <span className="text-gray-700 font-medium">Temperature</span>
            </div>
            <span className="font-bold text-gray-900 text-lg">
              {selectedStation.original_telemetry?.temperature_2m?.toFixed(1)} &deg;C
            </span>
          </div>

          <div className="flex items-center justify-between bg-blue-50 p-4 rounded-lg border border-blue-100">
            <div className="flex items-center gap-3">
              <Gauge className="text-blue-500" />
              <span className="text-gray-700 font-medium">Pressure</span>
            </div>
            <span className="font-bold text-gray-900 text-lg">
              {selectedStation.original_telemetry?.surface_pressure?.toFixed(1)} hPa
            </span>
          </div>

          <div className="flex items-center justify-between bg-teal-50 p-4 rounded-lg border border-teal-100">
            <div className="flex items-center gap-3">
              <Droplets className="text-teal-500" />
              <span className="text-gray-700 font-medium">Humidity</span>
            </div>
            <span className="font-bold text-gray-900 text-lg">
              {selectedStation.original_telemetry?.relative_humidity_2m?.toFixed(0)}%
            </span>
          </div>
        </div>
      )}
      

    </div>
  );
}

export default LiveReadings;
