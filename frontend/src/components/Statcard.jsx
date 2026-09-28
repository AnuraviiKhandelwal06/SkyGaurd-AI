import React from 'react';

function StatCard({ title, value, icon: Icon, color, onClick }) {
  return (
    <button
      type="button"
      onClick={onClick}
      className="w-full bg-white rounded-xl border border-gray-200 p-5 shadow-sm text-left cursor-pointer hover:shadow-md transition-all"
    >
      <div className="flex items-center justify-between">
        <p className="text-gray-500 font-medium">
          {title}
        </p>
        <div className={`p-2 rounded-full ${color}`}>
          <Icon size={20} />
        </div>
      </div>
      <h2 className="text-3xl font-bold text-gray-800 mt-4">
        {value}
      </h2>
    </button>
  );
}

export default StatCard;
