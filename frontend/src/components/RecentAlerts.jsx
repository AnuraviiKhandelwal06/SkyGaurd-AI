
import { useNavigate } from "react-router-dom";
import { TriangleAlert, CircleX, ArrowRight } from "lucide-react";
import { stations } from "../data/mockdata";

function RecentAlerts() {
  const navigate = useNavigate();

  const alerts = stations.filter(
    (station) =>
      station.status === "Warning" ||
      station.status === "Faulty"
  );

  const alertStyles = {
    Warning: {
      icon: TriangleAlert,
      color: "text-yellow-600",
      background: "bg-yellow-50"
    },
    Faulty: {
      icon: CircleX,
      color: "text-red-600",
      background: "bg-red-50"
    }
  };

  return (
    <div className="bg-white rounded-xl border border-gray-200 shadow-sm p-5 h-full">

      <div className="flex items-center justify-between mb-5">
        <div>
          <h2 className="text-lg font-semibold text-gray-800">
            Recent Alerts
          </h2>

          <p className="text-sm text-gray-500">
            Stations requiring attention
          </p>
        </div>

        <button
          type="button"
          onClick={() => navigate("/anomalies")}
          className="text-teal-600 hover:underline cursor-pointer text-sm"
        >
          View All
        </button>
      </div>

      <div className="space-y-3">

        {alerts.map((station) => {
          const style = alertStyles[station.status];
          const Icon = style.icon;

          return (
            <button
              key={station.id}
              type="button"
              onClick={() =>
                navigate(
                  `/stations?status=${station.status}&station=${station.id}`
                )
              }
              className={`w-full flex items-center gap-3 p-4 rounded-lg text-left cursor-pointer hover:shadow-md transition ${style.background}`}
            >
              <Icon size={22} className={style.color} />

              <div className="flex-1">
                <p className="font-semibold text-gray-800">
                  {station.name}
                </p>

                <p className="text-sm text-gray-500">
                  {station.status} · {station.location}
                </p>
              </div>

              <ArrowRight size={18} className="text-gray-400" />
            </button>
          );
        })}

        {alerts.length === 0 && (
          <p className="text-gray-500 text-sm">
            No active alerts.
          </p>
        )}

      </div>

      <p className="text-xs text-gray-400 mt-4">
        Demo station-status alerts, not verified anomaly events.
      </p>

    </div>
  );
}

export default RecentAlerts;