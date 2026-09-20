
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

import { stations } from "../data/mockdata";
import { sensorHealth } from "../data/mocksensorhealth";

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

  const selectedId =
    searchParams.get("station") || stations[0]?.id || "";

  const selectedStation = stations.find(
    (station) => station.id === selectedId
  );

  const healthRecord = sensorHealth.find(
    (record) => record.stationId === selectedId
  );

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
          {stations.map((station) => (
            <option key={station.id} value={station.id}>
              {station.name} — {station.location}
            </option>
          ))}
        </select>

      </div>

      {/* Sensor details */}
      {selectedStation && healthRecord && (
        <>
          <div className="bg-white rounded-xl border border-gray-200 p-5">

            <div className="flex items-center gap-3">
              <Activity className="text-teal-600" />

              <div>
                <h2 className="text-lg font-semibold">
                  {selectedStation.name}
                </h2>

                <p className="text-sm text-gray-500">
                  {selectedStation.id}
                </p>
              </div>
            </div>

          </div>

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-5">

            {healthRecord.sensors.map((sensor) => {
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
                    {sensor.health}%
                  </p>

                  <div className="w-full bg-gray-100 rounded-full h-2 mt-4">
                    <div
                      className={`h-2 rounded-full ${
                        sensor.status === "Healthy"
                          ? "bg-green-500"
                          : sensor.status === "Warning"
                          ? "bg-yellow-500"
                          : "bg-red-500"
                      }`}
                      style={{ width: `${sensor.health}%` }}
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