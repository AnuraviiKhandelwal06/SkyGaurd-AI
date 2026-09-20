
function StatCard({ title, value, icon: Icon, color, onClick }) {
  return (
    <button
      type="button"
            
        onClick={onClick}
      className="w-full bg-white rounded-xl border border-gray-200 p-5 shadow-sm text-left cursor-pointer hover:shadow-lg hover:border-teal-400 transition-all"
    >
      <div className="flex items-center justify-between">
        <p className="text-sm text-gray-500">
          {title}
        </p>

        <div className={`p-2 rounded-lg ${color}`}>
          <Icon size={20} />
        </div>
      </div>

      
    <p className="text-red-600 font-bold">
    CLICK TEST 123
    </p>

    <h2 className="text-3xl font-bold text-gray-800 mt-4">
    {value}
    </h2>
    </button>
  );
}

export default StatCard;