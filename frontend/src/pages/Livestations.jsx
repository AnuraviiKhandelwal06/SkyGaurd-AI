
import { useState } from "react";
import { useSearchParams } from "react-router-dom";
import { Search, MapPin, X } from "lucide-react";

import { stations } from "../data/mockdata";

function LiveStations() {
  const [searchParams, setSearchParams] = useSearchParams();
  const [search, setSearch] = useState("");

  const selectedStatus = searchParams.get("status") || "All";
  const selectedId = searchParams.get("station");

  const selectedStation = stations.find(
    (station) => station.id === selectedId
  );

  const filteredStations = stations.filter((station) => {
    const matchesStatus =
      selectedStatus === "All" ||
      station.status === selectedStatus;

    const query = search.trim().toLowerCase();

    const matchesSearch =
      station.name.toLowerCase().includes(query) ||
      station.id.toLowerCase().includes(query) ||
      station.location.toLowerCase().includes(query) ||
      station.state.toLowerCase().includes(query);

    return matchesStatus && matchesSearch;
  });

  const statusColors = {
    Healthy: "bg-green-100 text-green-700",
    Warning: "bg-yellow-100 text-yellow-700",
    Faulty: "bg-red-100 text-red-700"
  };

  function selectStation(station) {
    const params = new URLSearchParams(searchParams);
    params.set("station", station.id);
    setSearchParams(params);
  }

  function closeDetails() {
    const params = new URLSearchParams(searchParams);
    params.delete("station");
    setSearchParams(params);
  }

  function changeStatus(status) {
    const params = new URLSearchParams();

    if (status !== "All") {
      params.set("status", status);
    }

    setSearchParams(params);
  }

  return (
    <div className="p-8">

      <h1 className="text-2xl font-bold text-gray-800">
        Live Stations Network
      </h1>

      <p className="text-gray-500 mt-1">
        Indian Automatic Weather Stations
      </p>

      <p className="text-xs text-gray-400 mt-1 mb-6">
        Demonstration data — not live IMD observations.
      </p>

      {/* Search bar */}
      <div className="relative mb-5 max-w-md">
        <Search
          size={19}
          className="absolute left-3 top-3 text-gray-400"
        />

        <input
          type="text"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          placeholder="Search station ID, city or state..."
          className="w-full pl-10 pr-4 py-2.5 border border-gray-200 rounded-lg bg-white focus:outline-none focus:border-teal-500"
        />
      </div>

      {/* Status filters */}
      <div className="flex flex-wrap gap-3 mb-6">
        {["All", "Healthy", "Warning", "Faulty"].map(
          (status) => (
            <button
              key={status}
              type="button"
              onClick={() => changeStatus(status)}
              className={`px-4 py-2 rounded-lg cursor-pointer ${
                selectedStatus === status
                  ? "bg-teal-600 text-white"
                  : "bg-white border border-gray-200 text-gray-600 hover:bg-gray-100"
              }`}
            >
              {status}
            </button>
          )
        )}
      </div>

      {/* Station table */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-x-auto">

        <table className="w-full text-left">
          <thead className="bg-gray-100 text-gray-600 text-sm">
            <tr>
              <th className="p-4">Station ID</th>
              <th className="p-4">Station Name</th>
              <th className="p-4">Location</th>
              <th className="p-4">Status</th>
              <th className="p-4">Temperature</th>
              <th className="p-4">Pressure</th>
              <th className="p-4">Humidity</th>
            </tr>
          </thead>

          <tbody>
            {filteredStations.map((station) => (
              <tr
                key={station.id}
                onClick={() => selectStation(station)}
                className={`border-t border-gray-100 cursor-pointer hover:bg-teal-50 ${
                  selectedId === station.id
                    ? "bg-teal-50"
                    : ""
                }`}
              >
                <td className="p-4 text-teal-700 font-medium">
                  {station.id}
                </td>

                <td className="p-4">{station.name}</td>
                <td className="p-4">{station.location}</td>

                <td className="p-4">
                  <span
                    className={`px-3 py-1 rounded-full text-xs font-medium ${
                      statusColors[station.status]
                    }`}
                  >
                    {station.status}
                  </span>
                </td>

                <td className="p-4">{station.temperature} °C</td>
                <td className="p-4">{station.pressure} hPa</td>
                <td className="p-4">{station.humidity}%</td>
              </tr>
            ))}
          </tbody>
        </table>

        {filteredStations.length === 0 && (
          <p className="p-6 text-center text-gray-500">
            No matching stations found.
          </p>
        )}
      </div>

      <p className="text-sm text-gray-500 mt-4">
        Showing {filteredStations.length} of {stations.length} stations
      </p>

      {/* Selected station details */}
      {selectedStation && (
        <div className="mt-6 bg-white rounded-xl border border-teal-200 shadow-sm p-6">

          <div className="flex items-start justify-between mb-5">
            <div>
              <h2 className="text-xl font-bold text-gray-800">
                {selectedStation.name}
              </h2>

              <p className="text-sm text-gray-500">
                {selectedStation.id}
              </p>
            </div>

            <button
              type="button"
              onClick={closeDetails}
              className="p-2 rounded-lg hover:bg-gray-100 cursor-pointer"
              aria-label="Close station details"
            >
              <X size={20} />
            </button>
          </div>

          <div className="flex items-center gap-2 text-gray-500 mb-5">
            <MapPin size={18} />
            <span>
              {selectedStation.location}, {selectedStation.state}
            </span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">

            <div className="bg-orange-50 rounded-lg p-4">
              <p className="text-sm text-gray-500">
                Temperature
              </p>
              <p className="text-2xl font-bold text-gray-800">
                {selectedStation.temperature} °C
              </p>
            </div>

            <div className="bg-blue-50 rounded-lg p-4">
              <p className="text-sm text-gray-500">
                Atmospheric Pressure
              </p>
              <p className="text-2xl font-bold text-gray-800">
                {selectedStation.pressure} hPa
              </p>
            </div>

            <div className="bg-teal-50 rounded-lg p-4">
              <p className="text-sm text-gray-500">
                Relative Humidity
              </p>
              <p className="text-2xl font-bold text-gray-800">
                {selectedStation.humidity}%
              </p>
            </div>

          </div>

          <div className="mt-5">
            <span
              className={`inline-block px-4 py-2 rounded-full text-sm font-medium ${
                statusColors[selectedStation.status]
              }`}
            >
              Status: {selectedStation.status}
            </span>
          </div>

        </div>
      )}

    </div>
  );
}

export default LiveStations;