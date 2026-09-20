
import {
  RadioTower,
  CircleCheck,
  TriangleAlert,
  CircleX,
  Activity
} from "lucide-react";

import { useNavigate } from "react-router-dom";
import StatCard from "../components/Statcard";
import { stations } from "../data/mockdata";
import IndiaMap from "../components/Indiamap";
import LiveReadings from "../components/Livereadings";
import RecentAlerts from "../components/RecentAlerts";

function Dashboard() {
  const navigate = useNavigate();

  const totalStations = stations.length;

  const healthyStations = stations.filter(
    (station) => station.status === "Healthy"
  ).length;

  const warningStations = stations.filter(
    (station) => station.status === "Warning"
  ).length;

  const faultyStations = stations.filter(
    (station) => station.status === "Faulty"
  ).length;

  const activeAnomalies = warningStations + faultyStations;

  return (
    <div className="p-8">
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-gray-800">
          Overview Dashboard
        </h1>

        <p className="text-gray-500 mt-1">
          Indian AWS Network Monitoring
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-5 gap-5">
        <StatCard
          title="Total Stations"
          value={totalStations}
          icon={RadioTower}
          color="bg-blue-100 text-blue-600"
          onClick={() => 
            navigate("/stations")
          }
        />

        <StatCard
          title="Healthy Stations"
          value={healthyStations}
          icon={CircleCheck}
          color="bg-green-100 text-green-600"
          onClick={() => navigate("/stations?status=Healthy")}
        />

        <StatCard
          title="Warning Stations"
          value={warningStations}
          icon={TriangleAlert}
          color="bg-yellow-100 text-yellow-600"
          onClick={() => navigate("/stations?status=Warning")}
        />

        <StatCard
          title="Faulty Stations"
          value={faultyStations}
          icon={CircleX}
          color="bg-red-100 text-red-600"
          onClick={() => navigate("/stations?status=Faulty")}
        />

        <StatCard
          title="Active Anomalies"
          value={activeAnomalies}
          icon={Activity}
          color="bg-purple-100 text-purple-600"
          onClick={() => navigate("/anomalies")}
        />
      </div>
      <div className="mt-6">
        <IndiaMap />
      </div>
            
        <div className="grid grid-cols-1 xl:grid-cols-2 gap-6 mt-6">
        <LiveReadings />
        <RecentAlerts />
        </div>
    </div>
  );
}

export default Dashboard;