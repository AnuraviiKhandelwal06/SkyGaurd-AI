import React from 'react';
import { useNavigate } from "react-router-dom";
import { normalizeStatus } from "../utils/statusHelper";
import { TriangleAlert, CircleX, ArrowRight } from "lucide-react";

function RecentAlerts({ stationsData }) {
  const navigate = useNavigate();
  const safeStations = stationsData || [];

  const alerts = safeStations.filter(
    (s) => normalizeStatus(s.status) === "Warning" || normalizeStatus(s.status) === "Faulty"
  );

  const alertStyles = {
    Warning: {
      icon: TriangleAlert,
      color: "text-yellow-600",
      background: "bg-yellow-50",
      display: "Warning"
    },
    Faulty: {
      icon: CircleX,
      color: "text-red-600",
      background: "bg-red-50",
      display: "Faulty"
    },
    critical: {
      icon: CircleX,
      color: "text-red-600",
      background: "bg-red-50",
      display: "Faulty"
    }
  };

  return (
    <div className="bg-white rounded-xl border border-gray-200 shadow-sm p-6 h-full flex flex-col">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h2 className="text-lg font-bold text-gray-800">
            Recent Alerts
          </h2>
          <p className="text-sm text-gray-500 mt-1">
            Stations requiring attention
          </p>
        </div>
        <button
          type="button"
          onClick={() => navigate("/anomalies")}
          className="text-teal-600 font-medium hover:underline cursor-pointer text-sm"
        >
          View All
        </button>
      </div>

      <div className="space-y-3 flex-1 overflow-y-auto">
        {alerts.map((station) => {
          const style = alertStyles[station.status] || alertStyles.Warning;
          const Icon = style.icon;
          const displayStatus = style.display;

          return (
            <button
              key={station.station_id}
              type="button"
              onClick={() =>
                navigate(
                  `/stations?status=${encodeURIComponent(displayStatus)}&station=${encodeURIComponent(station.station_id)}`
                )
              }
              className={`w-full flex items-center gap-4 p-4 rounded-lg text-left cursor-pointer hover:shadow-md transition ${style.background}`}
            >
              <Icon size={24} className={style.color} />
              <div className="flex-1">
                <p className="font-bold text-gray-900">
                  {station.location}
                </p>
                <p className="text-sm text-gray-600">
                  {displayStatus} - {station.location}
                </p>
              </div>
              <ArrowRight size={20} className="text-gray-400" />
            </button>
          );
        })}

        {alerts.length === 0 && (
          <p className="text-gray-500 text-sm py-4">
            No active alerts.
          </p>
        )}
      </div>

      <p className="text-xs text-gray-400 mt-6 pt-4 border-t border-gray-100">
        Demo station-status alerts, not verified anomaly events.
      </p>
    </div>
  );
}

export default RecentAlerts;
