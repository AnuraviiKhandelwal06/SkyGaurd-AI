
import {
  BrowserRouter,
  Routes,
  Route,
  Navigate
} from "react-router-dom";

import Sidebar from "./components/Sidebar";

import Dashboard from "./pages/dashboard";
import LiveStations from "./pages/Livestations";
import AnomalyDetection from "./pages/anomalydetection";
import SensorHealth from "./pages/sensorhealth";
import Settings from "./pages/settings";

function App() {
  return (
    <BrowserRouter>
      <div className="flex min-h-screen bg-[#F7FAFF]">

        <Sidebar />

        <main className="flex-1 min-w-0">
          <Routes>
            <Route
              path="/"
              element={<Navigate to="/dashboard" replace />}
            />

            <Route
              path="/dashboard"
              element={<Dashboard />}
            />

            <Route
              path="/stations"
              element={<LiveStations />}
            />

            <Route
              path="/anomalies"
              element={<AnomalyDetection />}
            />

            <Route
              path="/sensor-health"
              element={<SensorHealth />}
            />

            <Route
              path="/settings"
              element={<Settings />}
            />

            <Route
              path="*"
              element={<Navigate to="/dashboard" replace />}
            />
          </Routes>
        </main>

      </div>
    </BrowserRouter>
  );
}

export default App;