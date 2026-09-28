
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  TriangleAlert,
  SearchCheck,
  Wrench,
  CheckCircle,
  XCircle,
  ClipboardList
} from "lucide-react";

import { useStationsData } from "../hooks/useStationsData";
import { normalizeStatus } from "../utils/statusHelper";
import { BASE_URL } from "../config/api";

function AnomalyDetection() {
  const navigate = useNavigate();
  const { data: stations, loading, error, refetch } = useStationsData();
  const anomalies = (stations || []).filter(s => { const st = normalizeStatus(s.status, s.anomaly_type); return st === "Warning" || st === "Faulty"; });
  const [selectedId, setSelectedId] = useState(
    null
  );

  const selected = anomalies.find((r) => r.station_id === selectedId);

  async function updateReviewStatus(status) {
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
  }

  const statusColors = {
    Pending: "bg-yellow-100 text-yellow-700",
    Accepted: "bg-green-100 text-green-700",
    Rejected: "bg-red-100 text-red-700",
    "Manual Review": "bg-blue-100 text-blue-700"
  };

  if (loading) return <div className="p-8">Loading...</div>;
  if (error) return <div className="p-8 text-red-500">Error</div>;
  return (
    <div className="p-8 space-y-6">

      <div>
        <h1 className="text-2xl font-bold text-gray-800">
          Anomaly Detection & Resolution
        </h1>

        <p className="text-gray-500 mt-1">
          Detection, fault diagnosis and data correction
        </p>

        <p className="text-xs text-amber-700 mt-2">
          Demonstration mode: anomaly results and corrections
          are sample data, not live AI predictions.
        </p>
      </div>

      {/* Detected anomalies */}
      <section className="bg-white rounded-xl border border-gray-200 p-6">

        <h2 className="text-lg font-semibold mb-4 flex items-center gap-2">
          <TriangleAlert className="text-amber-500" />
          Detected Anomalies
        </h2>

        <div className="space-y-3">
          {anomalies.map((record) => (
            <button
              key={record.station_id}
              type="button"
              onClick={() => setSelectedId(record.station_id)}
              className={`w-full p-4 rounded-lg border text-left cursor-pointer transition ${
                selectedId === record.station_id
                  ? "border-teal-500 bg-teal-50"
                  : "border-gray-200 hover:bg-gray-50"
              }`}
            >
              <div className="flex flex-wrap justify-between gap-2">

                <div>
                  {(() => { const score = record.severity_score ? record.severity_score * 100 : (record.explainability?.confidence_pct || 85.0); const reviewStatus = normalizeStatus(record.status) === "Healthy" ? "Accepted" : "Pending"; return <><div className="flex flex-col gap-2 w-full"><p className="font-semibold text-gray-800">{record.location} ({record.station_id})</p><div className="flex items-center gap-2 mt-1 mb-1 text-sm text-gray-500"><span className="bg-gray-200 px-2 py-0.5 rounded text-xs font-semibold">{record.anomaly_type || "UNKNOWN"}</span><span>Score: {score.toFixed(1)}/100</span></div><div className="w-full bg-gray-200 rounded-full h-1.5 max-w-md mb-2"><div className="h-1.5 rounded-full bg-red-500" style={{ width: `${Math.min(score, 100)}%` }} /></div></div></> })()}
                </div>

                <span
                  className={`text-xs px-3 py-1 rounded-full h-fit ${
                    statusColors[normalizeStatus(record.status) === "Healthy" ? "Accepted" : "Pending"] || statusColors.Pending
                  }`}
                >
                  {normalizeStatus(record.status) === "Healthy" ? "Accepted" : "Pending"}
                </span>

              </div>
            </button>
          ))}
        </div>
      </section>

      {selected && (
        <>
          {/* Fault diagnosis */}
          <section className="bg-white rounded-xl border border-gray-200 p-6">

            <h2 className="text-lg font-semibold mb-4 flex items-center gap-2">
              <SearchCheck className="text-blue-600" />
              Fault Diagnosis
            </h2>

            <div className="space-y-3 text-gray-700">

              <p>
                <strong>Station:</strong> {selected.location}
              </p>

              <p>
                <strong>Station ID:</strong> {selected.station_id}
              </p>

              <p>
                
              </p>

              <p>
                <strong>Suspected fault:</strong>{" "}
                {selected.anomaly_type}
              </p>

              <p>
                <strong>Demo confidence:</strong>{" "}
                {((selected.confidence_score || 0) * 100).toFixed(0)}%
              </p>

              <div className="bg-blue-50 p-4 rounded-lg">
                <p className="font-semibold mb-2">
                  Supporting Evidence
                </p>

                <ul className="list-disc pl-5 space-y-1">
                  {(selected.diagnosis?.diagnosis?.evidence_chain || ["Evidence auto-generated"]).map((item, index) => (<li key={index}>{item}</li>))}
                </ul>
              </div>

              <button
                type="button"
                onClick={() =>
                  navigate(
                    `/stations?station=${selected.station_id}`
                  )
                }
                className="text-teal-600 hover:underline cursor-pointer"
              >
                View Station Details →
              </button>

            </div>
          </section>

          {/* Data correction */}
          <section className="bg-white rounded-xl border border-gray-200 p-6">

            <h2 className="text-lg font-semibold mb-4 flex items-center gap-2">
              <Wrench className="text-teal-600" />
              Data Correction
            </h2>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-5">

              <div className="bg-red-50 rounded-lg p-4">
                <p className="text-sm text-gray-500">
                  Flagged Reading
                </p>

                <p className="text-2xl font-bold text-red-600 mt-1">
                  {selected.original_telemetry?.temperature_2m?.toFixed(1) || "--"}
                </p>
              </div>

              <div className="bg-green-50 rounded-lg p-4">
                <p className="text-sm text-gray-500">
                  Suggested Correction (Demo)
                </p>

                <p className="text-2xl font-bold text-green-600 mt-1">
                  {selected.correction?.corrected_value?.toFixed(1) || "--"}
                </p>
              </div>

            </div>

            <p className="text-sm text-gray-500 mb-4">
              Review the proposed correction before choosing an action.
              Accepting it only changes the local review status in this demo.
            </p>

            <div className="flex flex-wrap gap-3">

              <button
                type="button"
                onClick={() => updateReviewStatus("Accepted")}
                className="flex items-center gap-2 px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 cursor-pointer"
              >
                <CheckCircle size={18} />
                Accept
              </button>

              <button
                type="button"
                onClick={() => updateReviewStatus("Rejected")}
                className="flex items-center gap-2 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 cursor-pointer"
              >
                <XCircle size={18} />
                Reject
              </button>

              <button
                type="button"
                onClick={() =>
                  updateReviewStatus("Manual Review")
                }
                className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 cursor-pointer"
              >
                <ClipboardList size={18} />
                Manual Review
              </button>

            </div>

            <p className="mt-4 text-sm text-gray-600">
              Current review status:{" "}
              <strong>{normalizeStatus(selected.status) === "Healthy" ? "Accepted" : "Pending"}</strong>
            </p>

          </section>
        </>
      )}

    </div>
  );
}

export default AnomalyDetection;