
import {
  CloudLightning,
  LayoutDashboard,
  MapPin,
  TriangleAlert,
  HeartPulse,
  Settings
} from "lucide-react";

import { NavLink } from "react-router-dom";

function Sidebar() {

  const menuItems = [
    {
      name: "Overview",
      icon: LayoutDashboard,
      path: "/dashboard"
    },
    {
      name: "Live Stations",
      icon: MapPin,
      path: "/stations"
    },
    {
      name: "Anomaly Detection",
      icon: TriangleAlert,
      path: "/anomalies"
    },
    {
      name: "Sensor Health",
      icon: HeartPulse,
      path: "/sensor-health"
    },
    {
      name: "Settings",
      icon: Settings,
      path: "/settings"
    }
  ];

  return (
    <aside className="w-64 shrink-0 min-h-screen bg-[#151D2D] text-white p-5">

      <div className="flex items-center gap-3 mb-10">

        <div className="bg-teal-600 p-2 rounded-lg">
          <CloudLightning size={24} />
        </div>

        <div>
          <h1 className="text-lg font-bold">
            SkyGuard AI
          </h1>

          <p className="text-xs text-teal-400">
            WEATHER AWS SECURE
          </p>
        </div>

      </div>

      <nav className="space-y-2">

        {menuItems.map((item) => {

          const Icon = item.icon;

          return (
            <NavLink
              key={item.path}
              to={item.path}
              className={({ isActive }) =>
                `flex items-center gap-3 w-full px-4 py-3 rounded-lg transition-colors ${
                  isActive
                    ? "bg-[#163244] text-teal-400"
                    : "text-gray-300 hover:bg-[#263449]"
                }`
              }
            >
              <Icon size={20} />
              <span>{item.name}</span>
            </NavLink>
          );
        })}

      </nav>

    </aside>
  );
}

export default Sidebar;