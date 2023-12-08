// Dropdown.js

import React from "react";

const Dropdown = ({ label, options, value, onChange }) => {
  return (
    <div className="flex justify-center items-center p-4 bg-slate-100 rounded-md shadow-black">
      <label className="whitespace-nowrap mr-5">{label}:</label>
      <select
        className="w-full h-10 rounded"
        value={value}
        onChange={(e) => onChange(e.target.value)}
      >
        {options.map((option) => (
          <option key={option.value} value={option.value}>
            {option.label}
          </option>
        ))}
      </select>
    </div>
  );
};

export default Dropdown;
