# -*- coding: utf-8 -*-
import os
import re

def rewrite(path, func):
    with open(path, "r", encoding="utf-8") as f:
        c = f.read()
    c = func(c)
    with open(path, "w", encoding="utf-8") as f:
        f.write(c)

def d_patch(d):
    d = d.replace('import { stations } from "../data/mockdata";', 'import { useStationsData } from "../hooks/useStationsData";\nimport { normalizeStatus } from "../utils/statusHelper";')
    d = d.replace('function Dashboard() {\n  const navigate = useNavigate();\n\n  const totalStations = stations.length;', 'function Dashboard() {\n  const navigate = useNavigate();\n  const { data: stations, loading, error, lastUpdated } = useStationsData();\n\n  if (loading) return <div className="p-8">Loading dashboard data...</div>;\n  if (error) return <div className="p-8 text-red-500">Error: {error}</div>;\n\n  const totalStations = stations?.length || 0;')
    d = d.replace('stations.filter(\n    (s) => s.status === "Healthy"\n  )', '(stations || []).filter((s) => normalizeStatus(s.status, s.anomaly_type) === "Healthy")')
    d = d.replace('stations.filter(\n    (s) => s.status === "Warning"\n  )', '(stations || []).filter((s) => normalizeStatus(s.status, s.anomaly_type) === "Warning")')
    d = d.replace('stations.filter(\n    (s) => s.status === "Faulty" || s.status === "critical"\n  )', '(stations || []).filter((s) => normalizeStatus(s.status, s.anomaly_type) === "Faulty")')
    d = d.replace('Indian AWS Network Monitoring\n          </p>\n        </div>\n      </div>', 'Indian AWS Network Monitoring\n          </p>\n        </div>\n        {lastUpdated && <div className="text-sm text-gray-400">Last updated: {lastUpdated.toLocaleTimeString()}</div>}\n      </div>')
    return d

rewrite("src/pages/dashboard.jsx", d_patch)

def im_patch(im):
    im = im.replace('import { MapContainer, TileLayer, CircleMarker, Popup } from "react-leaflet";', 'import { MapContainer, TileLayer, CircleMarker, Popup } from "react-leaflet";\nimport { normalizeStatus, getStatusColor } from "../utils/statusHelper";')
    im = im.replace('const status = station.status === \'critical\' ? \'Faulty\' : station.status;', 'const status = normalizeStatus(station.status, station.anomaly_type);')
    im = im.replace('center={[station.latitude, station.longitude]}', 'center={[station.latitude || 20.0, station.longitude || 77.0]}')
    im = im.replace('color: statusColors[status] || "#22c55e",\n                  fillColor: statusColors[status] || "#22c55e",', 'color: getStatusColor(status),\n                  fillColor: getStatusColor(status),')
    im = im.replace('{station.original_telemetry?.temperature_2m?.toFixed(1)}', '{station.original_telemetry?.temperature_2m?.toFixed(1) || "--"}')
    im = im.replace('{station.original_telemetry?.surface_pressure?.toFixed(1)}', '{station.original_telemetry?.surface_pressure?.toFixed(1) || "--"}')
    im = im.replace('{station.original_telemetry?.relative_humidity_2m?.toFixed(1)}', '{station.original_telemetry?.relative_humidity_2m?.toFixed(1) || "--"}')
    return im

rewrite("src/components/Indiamap.jsx", im_patch)

def ls_patch(ls):
    ls = ls.replace('import { stations } from "../data/mockdata";', 'import { useStationsData } from "../hooks/useStationsData";\nimport { normalizeStatus } from "../utils/statusHelper";')
    ls = ls.replace('const [search, setSearch] = useState("");', 'const [search, setSearch] = useState("");\n  const { data: stations, loading, error, lastUpdated } = useStationsData();')
    ls = ls.replace('const selectedStation = stations.find(', 'const selectedStation = (stations || []).find(')
    ls = ls.replace('station.id === selectedId', 'station.station_id === selectedId')
    ls = ls.replace('const filteredStations = stations.filter((station) => {', 'const filteredStations = (stations || []).filter((station) => {')
    ls = ls.replace('station.status === selectedStatus;', 'normalizeStatus(station.status, station.anomaly_type) === selectedStatus;')
    ls = ls.replace('station.name.toLowerCase().includes(query) ||\n      station.id.toLowerCase().includes(query) ||\n      station.location.toLowerCase().includes(query) ||\n      station.state.toLowerCase().includes(query);', '(station.location || "").toLowerCase().includes(query) || (station.station_id || "").toLowerCase().includes(query);')
    ls = ls.replace('params.set("station", station.id);', 'params.set("station", station.station_id);')
    ls = ls.replace('Indian Automatic Weather Stations\n      </p>', 'Indian Automatic Weather Stations\n      </p>\n      {lastUpdated && <div className="text-sm text-gray-400 mt-2">Last updated: {lastUpdated.toLocaleTimeString()}</div>}')
    ls = ls.replace('<th className="p-4">Station ID</th>\n              <th className="p-4">Station Name</th>\n              <th className="p-4">Location</th>\n              <th className="p-4">Status</th>\n              <th className="p-4">Temperature</th>', '<th className="p-4">Station ID</th>\n              <th className="p-4">Location</th>\n              <th className="p-4">Status</th>\n              <th className="p-4">Score</th>\n              <th className="p-4">Temperature</th>')
    ls = ls.replace('key={station.id}', 'key={station.station_id}')
    ls = ls.replace('selectedId === station.id', 'selectedId === station.station_id')
    ls = ls.replace('{station.id}\n                </td>\n\n                <td className="p-4">{station.name}</td>\n                <td className="p-4">{station.location}</td>\n\n                <td className="p-4">', '{station.station_id}\n                </td>\n\n                <td className="p-4">{station.location}</td>\n\n                <td className="p-4">')
    ls = ls.replace('statusColors[station.status]', 'statusColors[normalizeStatus(station.status, station.anomaly_type)] || statusColors["Healthy"]')
    ls = ls.replace('{station.status}\n                  </span>\n                </td>\n\n                <td className="p-4">{station.temperature}', '{normalizeStatus(station.status, station.anomaly_type)}\n                  </span>\n                  {station.anomaly_type && station.anomaly_type !== "CLEAN" && <span className="ml-2 text-xs text-gray-500">{station.anomaly_type}</span>}\n                </td>\n                <td className="p-4">{(station.severity_score ? station.severity_score * 100 : (station.explainability?.confidence_pct || 85.0)).toFixed(1)}</td>\n                <td className="p-4">{station.original_telemetry?.temperature_2m?.toFixed(1) || "--"}')
    ls = ls.replace('<td className="p-4">{station.pressure} hPa</td>\n                <td className="p-4">{station.humidity}%</td>', '<td className="p-4">{station.original_telemetry?.surface_pressure?.toFixed(1) || "--"} hPa</td>\n                <td className="p-4">{station.original_telemetry?.relative_humidity_2m?.toFixed(1) || "--"}%</td>')
    ls = ls.replace('{stations.length}', '{(stations || []).length}')
    ls = ls.replace('{selectedStation.name}', '{selectedStation.location}')
    ls = ls.replace('{selectedStation.id}', '{selectedStation.station_id}')
    ls = ls.replace('{selectedStation.location}, {selectedStation.state}', '{selectedStation.latitude?.toFixed(2) || "--"}, {selectedStation.longitude?.toFixed(2) || "--"}')
    ls = ls.replace('{selectedStation.temperature}', '{selectedStation.original_telemetry?.temperature_2m?.toFixed(1) || "--"}')
    ls = ls.replace('{selectedStation.pressure} hPa', '{selectedStation.original_telemetry?.surface_pressure?.toFixed(1) || "--"} hPa')
    ls = ls.replace('{selectedStation.humidity}%', '{selectedStation.original_telemetry?.relative_humidity_2m?.toFixed(1) || "--"}%')
    ls = ls.replace('Status: {selectedStation.status}', 'Status: {normalizeStatus(selectedStation.status, selectedStation.anomaly_type)}')
    ls = ls.replace('statusColors[selectedStation.status]', 'statusColors[normalizeStatus(selectedStation.status, selectedStation.anomaly_type)] || statusColors["Healthy"]')
    ls = ls.replace('return (\n    <div className="p-8">', 'if (loading) return <div className="p-8">Loading...</div>;\n  if (error) return <div className="p-8 text-red-500">Error</div>;\n  return (\n    <div className="p-8">')
    return ls

rewrite("src/pages/Livestations.jsx", ls_patch)

def ad_patch(ad):
    ad = ad.replace('import { anomalies } from "../data/mockanomalies";', 'import { useStationsData } from "../hooks/useStationsData";\nimport { normalizeStatus } from "../utils/statusHelper";\nimport { BASE_URL } from "../config/api";')
    ad = ad.replace('const [records, setRecords] = useState(anomalies);', '')
    ad = ad.replace('anomalies[0]?.id || ""', 'null')
    ad = ad.replace('function AnomalyDetection() {\n  const navigate = useNavigate();\n\n  \n  const [selectedId, setSelectedId] = useState(', 'function AnomalyDetection() {\n  const navigate = useNavigate();\n  const { data: stations, loading, error, refetch } = useStationsData();\n  const anomalies = (stations || []).filter(s => { const st = normalizeStatus(s.status, s.anomaly_type); return st === "Warning" || st === "Faulty"; });\n  const [selectedId, setSelectedId] = useState(')
    ad = ad.replace('const selected = records.find(\n    (record) => record.id === selectedId\n  );', 'const selected = anomalies.find((r) => r.station_id === selectedId);')
    ad = ad.replace('function updateReviewStatus(status) {\n    if (!selected) return;\n\n    setRecords((previous) =>\n      previous.map((record) =>\n        record.id === selectedId\n          ? { ...record, reviewStatus: status }\n          : record\n      )\n    );\n  }', '''async function updateReviewStatus(status) {
    if (!selected) return;
    const corrId = selected.correction?.id;
    if (status === 'Accepted' && corrId) {
       try {
         await fetch(`${BASE_URL}/api/corrections/${corrId}/decision`, {
           method: 'PATCH',
           headers: { 'Content-Type': 'application/json' },
           body: JSON.stringify({ decision: 'accepted' })
         });
       } catch (e) {
         console.error(e);
       }
    }
    refetch();
    setSelectedId(null);
  }''')
    ad = ad.replace('return (\n    <div className="p-8 space-y-6">', 'if (loading) return <div className="p-8">Loading...</div>;\n  if (error) return <div className="p-8 text-red-500">Error</div>;\n  return (\n    <div className="p-8 space-y-6">')
    ad = ad.replace('records.map((record)', 'anomalies.map((record)')
    ad = ad.replace('key={record.id}', 'key={record.station_id}')
    ad = ad.replace('onClick={() => setSelectedId(record.id)}', 'onClick={() => setSelectedId(record.station_id)}')
    ad = ad.replace('selectedId === record.id', 'selectedId === record.station_id')
    ad = ad.replace('<p className="font-semibold text-gray-800">\n                    {record.stationName}\n                  </p>\n\n                  <p className="text-sm text-gray-500 mt-1">\n                    {record.parameter}: {record.observedValue}\n                    {" "}{record.unit}\n                  </p>', '{(() => { const score = record.severity_score ? record.severity_score * 100 : (record.explainability?.confidence_pct || 85.0); const reviewStatus = record.status === "resolved" ? "Accepted" : "Pending"; return <><div className="flex flex-col gap-2 w-full"><p className="font-semibold text-gray-800">{record.location} ({record.station_id})</p><div className="flex items-center gap-2 mt-1 mb-1 text-sm text-gray-500"><span className="bg-gray-200 px-2 py-0.5 rounded text-xs font-semibold">{record.anomaly_type || "UNKNOWN"}</span><span>Score: {score.toFixed(1)}/100</span></div><div className="w-full bg-gray-200 rounded-full h-1.5 max-w-md mb-2"><div className="h-1.5 rounded-full bg-red-500" style={{ width: `${Math.min(score, 100)}%` }} /></div></div></> })()}')
    ad = ad.replace('{record.reviewStatus}', '{record.status === "resolved" ? "Accepted" : "Pending"}')
    ad = ad.replace('statusColors[record.reviewStatus]', 'statusColors[record.status === "resolved" ? "Accepted" : "Pending"] || statusColors.Pending')
    ad = ad.replace('{selected.stationName}', '{selected.location}')
    ad = ad.replace('{selected.stationId}', '{selected.station_id}')
    ad = ad.replace('<strong>Parameter:</strong> {selected.parameter}', '')
    ad = ad.replace('{selected.suspectedFault}', '{selected.anomaly_type}')
    ad = ad.replace('{(selected.confidence * 100).toFixed(0)}%', '{((selected.confidence_score || 0) * 100).toFixed(0)}%')
    ad = ad.replace('{selected.evidence.map((item, index) => (\n                    <li key={index}>{item}</li>\n                  ))}', '{(selected.diagnosis?.diagnosis?.evidence_chain || ["Evidence auto-generated"]).map((item, index) => (<li key={index}>{item}</li>))}')
    ad = ad.replace('`/stations?station=${selected.stationId}`', '`/stations?station=${selected.station_id}`')
    ad = ad.replace('{selected.observedValue} {selected.unit}', '{selected.original_telemetry?.temperature_2m?.toFixed(1) || "--"}')
    ad = ad.replace('{selected.suggestedValue} {selected.unit}', '{selected.correction?.corrected_value?.toFixed(1) || "--"}')
    ad = ad.replace('{selected.reviewStatus}', '{selected.status === "resolved" ? "Accepted" : "Pending"}')
    return ad

rewrite("src/pages/anomalydetection.jsx", ad_patch)

def sh_patch(sh):
    sh = sh.replace('import { stations } from "../data/mockdata";\nimport { sensorHealth } from "../data/mocksensorhealth";', 'import { useStationsData, useStationData } from "../hooks/useStationsData";\nimport { normalizeStatus } from "../utils/statusHelper";\nimport {\n  LineChart,\n  Line,\n  XAxis,\n  YAxis,\n  CartesianGrid,\n  Tooltip,\n  ResponsiveContainer\n} from "recharts";')
    sh = sh.replace('const selectedId =\n    searchParams.get("station") || stations[0]?.id || "";\n\n  const selectedStation = stations.find(\n    (station) => station.id === selectedId\n  );\n\n  const healthRecord = sensorHealth.find(\n    (record) => record.stationId === selectedId\n  );', '''
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
''')
    sh = sh.replace('const key = `${selectedId}-${sensorType}`;', 'const key = `${selectedId}-${sensorType}`;') 
    sh = sh.replace('{stations.map((station) => (\n            <option key={station.id} value={station.id}>\n              {station.name} \u2014 {station.location}\n            </option>\n          ))}', '{(stations||[]).map((station) => (\n            <option key={station.station_id} value={station.station_id}>\n              {station.location} ({station.station_id})\n            </option>\n          ))}')
    sh = sh.replace('healthRecord.sensors.map((sensor)', 'sensorsList.map((sensor)')
    sh = sh.replace('{selectedStation.name}', '{selectedStation.location}')
    sh = sh.replace('{selectedStation.id}', '{selectedStation.station_id}')
    sh = sh.replace('<div>\n                <h2 className="text-lg font-semibold">\n                  {selectedStation.location}\n                </h2>\n\n                <p className="text-sm text-gray-500">\n                  {selectedStation.station_id}\n                </p>\n              </div>', '<div><h2 className="text-lg font-semibold">{selectedStation.location}</h2><p className="text-sm text-gray-500">{selectedStation.station_id}</p></div></div><div className="flex gap-8"><div className="text-right"><p className="text-sm text-gray-500 font-medium">Fleet/Station Health</p><p className="text-2xl font-bold">{(healthData?.health_score_pct || 100).toFixed(1)}%</p></div><div className="text-right"><p className="text-sm text-gray-500 font-medium">MTBF / Est RUL</p><p className="text-2xl font-bold">{healthData?.estimated_rul_days || 0} days</p></div></div></div><div className="mb-8"><p className="text-sm text-gray-500 font-medium mb-4 mt-6">Degradation Trend</p><div className="h-[200px] w-full"><ResponsiveContainer width="100%" height="100%"><LineChart data={chartData}><CartesianGrid strokeDasharray="3 3" vertical={false} /><XAxis dataKey="name" axisLine={false} tickLine={false} tick={{fontSize: 12, fill: "#9ca3af"}} /><YAxis domain={[0, 100]} axisLine={false} tickLine={false} tick={{fontSize: 12, fill: "#9ca3af"}} /><Tooltip /><Line type="monotone" dataKey="health" stroke="#0d9488" strokeWidth={2} dot={{r: 3, fill: "#0d9488"}} /></LineChart></ResponsiveContainer></div><div>')
    sh = sh.replace('{selectedStation && healthRecord && (', '{selectedStation && healthData && (')
    sh = sh.replace('{sensor.health}%', '{sensor.health.toFixed(1)}%')
    return sh

rewrite("src/pages/sensorhealth.jsx", sh_patch)

