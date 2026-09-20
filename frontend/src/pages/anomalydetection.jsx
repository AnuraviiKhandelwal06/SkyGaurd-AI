
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

import { anomalies } from "../data/mockanomalies";

function AnomalyDetection() {
  const navigate = useNavigate();

  const [records, setRecords] = useState(anomalies);
  const [selectedId, setSelectedId] = useState(
    anomalies[0]?.id || ""
  );

  const selected = records.find(
    (record) => record.id === selectedId
  );

  function updateReviewStatus(status) {
    if (!selected) return;

    setRecords((previous) =>
      previous.map((record) =>
        record.id === selectedId
          ? { ...record, reviewStatus: status }
          : record
      )
    );
  }

  const statusColors = {
    Pending: "bg-yellow-100 text-yellow-700",
    Accepted: "bg-green-100 text-green-700",
    Rejected: "bg-red-100 text-red-700",
    "Manual Review": "bg-blue-100 text-blue-700"
  };

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
          {records.map((record) => (
            <button
              key={record.id}
              type="button"
              onClick={() => setSelectedId(record.id)}
              className={`w-full p-4 rounded-lg border text-left cursor-pointer transition ${
                selectedId === record.id
                  ? "border-teal-500 bg-teal-50"
                  : "border-gray-200 hover:bg-gray-50"
              }`}
            >
              <div className="flex flex-wrap justify-between gap-2">

                <div>
                  <p className="font-semibold text-gray-800">
                    {record.stationName}
                  </p>

                  <p className="text-sm text-gray-500 mt-1">
                    {record.parameter}: {record.observedValue}
                    {" "}{record.unit}
                  </p>
                </div>

                <span
                  className={`text-xs px-3 py-1 rounded-full h-fit ${
                    statusColors[record.reviewStatus]
                  }`}
                >
                  {record.reviewStatus}
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
                <strong>Station:</strong> {selected.stationName}
              </p>

              <p>
                <strong>Station ID:</strong> {selected.stationId}
              </p>

              <p>
                <strong>Parameter:</strong> {selected.parameter}
              </p>

              <p>
                <strong>Suspected fault:</strong>{" "}
                {selected.suspectedFault}
              </p>

              <p>
                <strong>Demo confidence:</strong>{" "}
                {(selected.confidence * 100).toFixed(0)}%
              </p>

              <div className="bg-blue-50 p-4 rounded-lg">
                <p className="font-semibold mb-2">
                  Supporting Evidence
                </p>

                <ul className="list-disc pl-5 space-y-1">
                  {selected.evidence.map((item, index) => (
                    <li key={index}>{item}</li>
                  ))}
                </ul>
              </div>

              <button
                type="button"
                onClick={() =>
                  navigate(
                    `/stations?station=${selected.stationId}`
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
                  {selected.observedValue} {selected.unit}
                </p>
              </div>

              <div className="bg-green-50 rounded-lg p-4">
                <p className="text-sm text-gray-500">
                  Suggested Correction (Demo)
                </p>

                <p className="text-2xl font-bold text-green-600 mt-1">
                  {selected.suggestedValue} {selected.unit}
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
              <strong>{selected.reviewStatus}</strong>
            </p>

          </section>
        </>
      )}

    </div>
  );
}

export default AnomalyDetection;