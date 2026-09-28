
import { MapContainer, TileLayer, CircleMarker, Popup } from "react-leaflet";
import { normalizeStatus, getStatusColor } from "../utils/statusHelper";
import { useNavigate } from "react-router-dom";
import { useStationsData } from "../hooks/useStationsData";
import "leaflet/dist/leaflet.css";

const statusColors = {
  Healthy: "#22c55e",
  Warning: "#f59e0b",
  Faulty: "#ef4444"
};

function IndiaMap() {
  const navigate = useNavigate();
  const { data: stationsData } = useStationsData();
  const stations = stationsData || [];

  return (
    <div className="bg-white rounded-xl border border-gray-200 shadow-sm p-5">

      <div className="flex items-center justify-between mb-4">
        <div>
          <h2 className="text-lg font-semibold text-gray-800">
            India AWS Network Map
          </h2>
          <p className="text-sm text-gray-500">
            Indian weather station locations
          </p>
        </div>

        <button
          type="button"
          onClick={() => navigate("/stations")}
          className="text-teal-600 hover:underline cursor-pointer"
        >
          View All Stations →
        </button>
      </div>

      <div className="h-[400px] rounded-lg overflow-hidden">
        <MapContainer
          center={[22.5, 79]}
          zoom={5}
          scrollWheelZoom={false}
          style={{ height: "100%", width: "100%" }}
        >
          <TileLayer
            attribution='&copy; OpenStreetMap contributors'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          />

          {stations.map((station) => {
            if (!station.latitude || !station.longitude) {
              console.warn(`Station ${station.station_id} missing coordinates. Skipping map marker.`);
              return null;
            }
            const normStatus = normalizeStatus(station.status, station.anomaly_type);
            const color = statusColors[normStatus] || statusColors.Healthy;
            
            return (
              <CircleMarker
                key={station.station_id}
                center={[station.latitude, station.longitude]}
                radius={9}
                pathOptions={{
                  color: color,
                  fillColor: color,
                  fillOpacity: 0.85,
                  weight: 2
                }}
              >
                <Popup>
                  <div>
                    <h3 className="font-bold">{station.location}</h3>

                    <p>Station ID: {station.station_id}</p>
                    <p>Location: {station.location}</p>
                    <p>Status: {normStatus}</p>
                    {station.original_telemetry && (
                      <>
                        <p>Temperature: {station.original_telemetry.temperature_2m?.toFixed(1)} °C</p>
                        <p>Pressure: {station.original_telemetry.surface_pressure?.toFixed(1)} hPa</p>
                        <p>Humidity: {station.original_telemetry.relative_humidity_2m?.toFixed(1)}%</p>
                      </>
                    )}

                    <button
                      type="button"
                      
                      onClick={() =>
                      navigate(`/stations?station=${station.station_id}`)
                      }
                      className="mt-2 text-teal-600 underline cursor-pointer"
                    >
                      View Station
                    </button>
                  </div>
                </Popup>
              </CircleMarker>
            );
          })}
        </MapContainer>
      </div>

      <div className="flex flex-wrap gap-5 mt-4 text-sm text-gray-600">
        <span>🟢 Healthy</span>
        <span>🟠 Warning</span>
        <span>🔴 Faulty</span>
      </div>

      <p className="mt-3 text-xs text-gray-400">
        Demo stations and readings. Not live IMD observations.
      </p>
    </div>
  );
}

export default IndiaMap;