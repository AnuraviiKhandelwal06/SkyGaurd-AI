import re
import difflib

with open('src/components/Indiamap.jsx', 'r', encoding='utf-8') as f:
    old_content = f.read()

# 1. Replace import
new_content = old_content.replace(
    'import { stations } from "../data/mockdata";',
    'import { useStationsData } from "../hooks/useStationsData";'
)

# 2. Add hook call
new_content = new_content.replace(
    'function IndiaMap() {\n  const navigate = useNavigate();',
    'function IndiaMap() {\n  const navigate = useNavigate();\n  const { data: stationsData } = useStationsData();\n  const stations = stationsData || [];'
)

# 3. Replace map logic - Using regex to safely replace the block
start_idx = new_content.find('{stations.map((station) => (')
end_idx = new_content.find('</MapContainer>', start_idx)

if start_idx != -1 and end_idx != -1:
    map_logic_new = '''{stations.map((station) => {
            if (!station.latitude || !station.longitude) {
              console.warn(Station  missing coordinates. Skipping map marker.);
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
                        <p>Temperature: {station.original_telemetry.temperature_2m?.toFixed(1)} C</p>
                        <p>Pressure: {station.original_telemetry.surface_pressure?.toFixed(1)} hPa</p>
                        <p>Humidity: {station.original_telemetry.relative_humidity_2m?.toFixed(1)}%</p>
                      </>
                    )}

                    <button
                      type="button"
                      
                      onClick={() =>
                      navigate(/stations?station=)
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
        '''
    new_content = new_content[:start_idx] + map_logic_new + new_content[end_idx:]

with open('src/components/Indiamap.jsx', 'w', encoding='utf-8') as f:
    f.write(new_content)

diff = difflib.unified_diff(
    old_content.splitlines(),
    new_content.splitlines(),
    fromfile='Indiamap.jsx.old',
    tofile='Indiamap.jsx',
    lineterm=''
)
print('\n'.join(diff))
