import React from 'react';

const HealthScoreCard = ({ score }) => {
  const getScoreColor = () => {
    if (score >= 80) return '#22c55e'; // Green
    if (score >= 50) return '#eab308'; // Yellow
    return '#ef4444'; // Red
  };

  const getScoreLabel = () => {
    if (score >= 80) return 'Excellent';
    if (score >= 50) return 'Fair';
    return 'Critical';
  };

  const color = getScoreColor();
  const radius = 60;
  const circumference = 2 * Math.PI * radius;
  const strokeDashoffset = circumference - (score / 100) * circumference;

  return (
    <div className="glass-card p-6 flex flex-col items-center justify-center">
      <h3 className="text-lg font-semibold text-slate-300 mb-6">Field Health Score</h3>
      
      <div className="relative flex items-center justify-center">
        {/* Background Circle */}
        <svg className="transform -rotate-90 w-40 h-40">
          <circle
            cx="80"
            cy="80"
            r={radius}
            stroke="rgba(30, 41, 59, 0.5)"
            strokeWidth="12"
            fill="transparent"
          />
          {/* Progress Circle */}
          <circle
            cx="80"
            cy="80"
            r={radius}
            stroke={color}
            strokeWidth="12"
            fill="transparent"
            strokeDasharray={circumference}
            strokeDashoffset={strokeDashoffset}
            strokeLinecap="round"
            className="transition-all duration-1000 ease-out"
          />
        </svg>
        
        {/* Center Text */}
        <div className="absolute text-center">
          <div className="text-4xl font-bold font-heading" style={{ color }}>
            {score.toFixed(0)}<span className="text-xl">%</span>
          </div>
        </div>
      </div>
      
      <div className="mt-6 text-center">
        <span 
          className="px-4 py-1 rounded-full text-sm font-semibold tracking-wider uppercase border"
          style={{ color, borderColor: color, backgroundColor: `${color}20` }}
        >
          {getScoreLabel()}
        </span>
      </div>
    </div>
  );
};

export default HealthScoreCard;
