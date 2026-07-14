import React from 'react';
import {
  Chart as ChartJS,
  ArcElement,
  Tooltip,
  Legend,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
} from 'chart.js';
import { Doughnut, Line, Bar } from 'react-chartjs-2';

ChartJS.register(
  ArcElement, Tooltip, Legend,
  CategoryScale, LinearScale,
  PointElement, LineElement, BarElement, Title
);

// Chart Theme Configuration
const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      labels: {
        color: '#e2e8f0',
        font: { family: "'Inter', sans-serif" }
      }
    }
  },
  scales: {
    x: {
      grid: { color: 'rgba(51, 65, 85, 0.2)' },
      ticks: { color: '#94a3b8' }
    },
    y: {
      grid: { color: 'rgba(51, 65, 85, 0.2)' },
      ticks: { color: '#94a3b8' }
    }
  }
};

const doughnutOptions = {
  ...chartOptions,
  scales: { x: { display: false }, y: { display: false } },
  cutout: '70%',
};

export const DiseaseFrequencyChart = ({ data }) => {
  const chartData = {
    labels: Object.keys(data || {}).map(l => l.replace(/_/g, ' ')),
    datasets: [
      {
        data: Object.values(data || {}),
        backgroundColor: [
          'rgba(239, 68, 68, 0.8)',
          'rgba(245, 158, 11, 0.8)',
          'rgba(16, 185, 129, 0.8)',
          'rgba(59, 130, 246, 0.8)',
          'rgba(139, 92, 246, 0.8)',
        ],
        borderColor: 'rgba(15, 23, 42, 1)',
        borderWidth: 2,
      },
    ],
  };

  return <Doughnut data={chartData} options={doughnutOptions} />;
};

export const SeverityTrendsChart = ({ data }) => {
  const chartData = {
    labels: data?.labels || [],
    datasets: [
      {
        label: 'Average Severity Score',
        data: data?.values || [],
        borderColor: '#f59e0b',
        backgroundColor: 'rgba(245, 158, 11, 0.1)',
        fill: true,
        tension: 0.4,
      }
    ],
  };

  return <Line data={chartData} options={chartOptions} />;
};

export const CropHealthOverviewChart = ({ data }) => {
  const chartData = {
    labels: data?.labels || [],
    datasets: [
      {
        label: 'Healthy Scans',
        data: data?.healthy || [],
        backgroundColor: 'rgba(34, 197, 94, 0.7)',
      },
      {
        label: 'Diseased Scans',
        data: data?.diseased || [],
        backgroundColor: 'rgba(239, 68, 68, 0.7)',
      }
    ],
  };

  return <Bar data={chartData} options={{...chartOptions, stacked: true}} />;
};
