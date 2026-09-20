
import { useState } from "react";
import { Bell, RefreshCw, MapPin, Save } from "lucide-react";
import { stations } from "../data/mockdata";

const DEFAULT_SETTINGS = {
  notifications: true,
  refreshInterval: "60",
  defaultStation: stations[0]?.id || ""
};

function Settings() {
  const [settings, setSettings] = useState(() => {
    try {
      const saved = localStorage.getItem("skyguard-settings");
      return saved
        ? { ...DEFAULT_SETTINGS, ...JSON.parse(saved) }
        : DEFAULT_SETTINGS;
    } catch {
      return DEFAULT_SETTINGS;
    }
  });

  const [savedMessage, setSavedMessage] = useState("");

  function updateSetting(key, value) {
    setSettings((previous) => ({
      ...previous,
      [key]: value
    }));

    setSavedMessage("");
  }

  function saveSettings() {
    try {
      localStorage.setItem(
        "skyguard-settings",
        JSON.stringify(settings)
      );

      setSavedMessage("Settings saved successfully!");
    } catch {
      setSavedMessage("Could not save settings.");
    }
  }

  return (
    <div className="p-8 max-w-4xl">

      <div className="mb-8">
        <h1 className="text-2xl font-bold text-gray-800">
          Settings
        </h1>

        <p className="text-gray-500 mt-1">
          Configure your SkyGuard AI dashboard preferences
        </p>
      </div>

      <div className="bg-white rounded-xl border border-gray-200 shadow-sm p-6 space-y-7">

        {/* Alert notifications */}
        <div className="flex items-center justify-between gap-4">

          <div className="flex items-center gap-3">
            <Bell className="text-teal-600" size={22} />

            <div>
              <h2 className="font-semibold text-gray-800">
                Alert Notifications
              </h2>

              <p className="text-sm text-gray-500">
                Enable dashboard anomaly notifications
              </p>
            </div>
          </div>

          <input
            type="checkbox"
            checked={settings.notifications}
            onChange={(e) =>
              updateSetting(
                "notifications",
                e.target.checked
              )
            }
            className="w-5 h-5 accent-teal-600 cursor-pointer"
          />

        </div>

        <hr className="border-gray-200" />

        {/* Refresh interval */}
        <div>
          <div className="flex items-center gap-3 mb-3">
            <RefreshCw className="text-teal-600" size={22} />

            <div>
              <h2 className="font-semibold text-gray-800">
                Auto Refresh Interval
              </h2>

              <p className="text-sm text-gray-500">
                Configure future backend data refresh
              </p>
            </div>
          </div>

          <select
            value={settings.refreshInterval}
            onChange={(e) =>
              updateSetting(
                "refreshInterval",
                e.target.value
              )
            }
            className="w-full border border-gray-200 rounded-lg p-3 bg-white cursor-pointer"
          >
            <option value="30">Every 30 seconds</option>
            <option value="60">Every 1 minute</option>
            <option value="300">Every 5 minutes</option>
            <option value="600">Every 10 minutes</option>
          </select>
        </div>

        <hr className="border-gray-200" />

        {/* Default station */}
        <div>
          <div className="flex items-center gap-3 mb-3">
            <MapPin className="text-teal-600" size={22} />

            <div>
              <h2 className="font-semibold text-gray-800">
                Default AWS Station
              </h2>

              <p className="text-sm text-gray-500">
                Select your preferred Indian weather station
              </p>
            </div>
          </div>

          <select
            value={settings.defaultStation}
            onChange={(e) =>
              updateSetting(
                "defaultStation",
                e.target.value
              )
            }
            className="w-full border border-gray-200 rounded-lg p-3 bg-white cursor-pointer"
          >
            {stations.map((station) => (
              <option key={station.id} value={station.id}>
                {station.name}
              </option>
            ))}
          </select>
        </div>

        <hr className="border-gray-200" />

        {/* Save button */}
        <div className="flex items-center gap-4">

          <button
            type="button"
            onClick={saveSettings}
            className="flex items-center gap-2 px-5 py-3 bg-teal-600 text-white rounded-lg hover:bg-teal-700 cursor-pointer"
          >
            <Save size={18} />
            Save Settings
          </button>

          {savedMessage && (
            <p
              role="status"
              className={`text-sm ${
                savedMessage.includes("successfully")
                  ? "text-green-600"
                  : "text-red-600"
              }`}
            >
              {savedMessage}
            </p>
          )}

        </div>

      </div>

    </div>
  );
}

export default Settings;