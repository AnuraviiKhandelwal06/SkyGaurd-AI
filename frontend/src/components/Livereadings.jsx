
import { useState } from "react";
import { Thermometer, Gauge, Droplets } from "lucide-react";
import { stations } from "../data/mockdata";

function LiveReadings() {
  
  const [selectedId, setSelectedId] = useState(() => {
    try {
      const saved = JSON.parse(
        localStorage.getItem("skyguard-settings") || "{}"
      );

      const exists = stations.some(
        (station) => station.id === saved.defaultStation
      );

      return exists
        ? saved.defaultStation
        : stations[0]?.id || "";
    } catch {
      return stations[0]?.id || "";
    }
  });

  const selectedStation = stations.find(
    (station) => station.id === selectedId
  );

  return (
    <div className="bg-white rounded-xl border border-gray-200 shadow-sm p-5 h-full">

      <div className="mb-5">
        <h2 className="text-lg font-semibold text-gray-800">
          Live Readings
        </h2>

        <p className="text-sm text-gray-500">
          Select an Indian AWS station
        </p>
      </div>

      <select
        value={selectedId}
        onChange={(e) => setSelectedId(e.target.value)}
        className="w-full border border-gray-200 rounded-lg p-3 mb-5 bg-white cursor-pointer"
      >
        {stations.map((station) => (
          <option key={station.id} value={station.id}>
            {station.name}
          </option>
        ))}
      </select>

      {selectedStation && (
        <div className="space-y-4">

          <div className="flex items-center justify-between bg-orange-50 p-4 rounded-lg">
            <div className="flex items-center gap-3">
              <Thermometer className="text-orange-500" />
              <span className="text-gray-600">Temperature</span>
            </div>

            <span className="font-bold text-gray-800">
              {selectedStation.temperature} °C
            </span>
          </div>

          <div className="flex items-center justify-between bg-blue-50 p-4 rounded-lg">
            <div className="flex items-center gap-3">
              <Gauge className="text-blue-500" />
              <span className="text-gray-600">Pressure</span>
            </div>

            <span className="font-bold text-gray-800">
              {selectedStation.pressure} hPa
            </span>
          </div>

          <div className="flex items-center justify-between bg-teal-50 p-4 rounded-lg">
            <div className="flex items-center gap-3">
              <Droplets className="text-teal-500" />
              <span className="text-gray-600">Humidity</span>
            </div>

            <span className="font-bold text-gray-800">
              {selectedStation.humidity}%
            </span>
          </div>

          <p className="text-xs text-gray-400">
            Demo readings — not live IMD observations.
          </p>

        </div>
      )}
    </div>
  );
}

export default LiveReadings;