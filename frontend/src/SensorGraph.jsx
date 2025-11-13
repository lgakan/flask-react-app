import React from 'react';
import { Line } from 'react-chartjs-2';
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend,
} from 'chart.js';

ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend
);

const SensorGraph = ({ dataPoints, onPointClick }) => {
    const handleChartClick = (event, elements) => {
        if (elements.length > 0) {
            const dataIndex = elements[0].index;
            onPointClick(dataPoints[dataIndex]);
        }
    };

    const formattedLabels = dataPoints.map(d => {
        const date = new Date(d.timestamp);
        return date.toLocaleString([], { hour: '2-digit', minute: '2-digit', day: '2-digit', month: '2-digit', year: 'numeric' });
    });

    const data = {
        labels: formattedLabels,
        datasets: [
            {
                label: 'Temperature (°C)',
                data: dataPoints.map(d => d.temperature),
                fill: false,
                borderColor: 'rgb(75, 192, 192)',
                tension: 0.1,
            },
            {
                label: 'Humidity (%)',
                data: dataPoints.map(d => d.humidity),
                fill: false,
                borderColor: 'rgb(54, 162, 235)',
                tension: 0.1,
            },
            {
                label: 'Pressure (hPa)',
                data: dataPoints.map(d => d.pressure),
                fill: false,
                borderColor: 'rgb(144,47,203)',
                tension: 0.1,
            },
            {
                label: 'light Level (%)',
                data: dataPoints.map(d => d.lightLevel),
                fill: false,
                borderColor: 'rgb(150,148,31)',
                tension: 0.1,
            },
        ],
    };

    const options = {
        responsive: true, // Ensure chart is responsive
        maintainAspectRatio: false, // Allow chart to fill container's height/width
        onClick: handleChartClick,
        animation: {
            duration: 0
        },
        scales: {
            x: {
                title: {
                    display: true,
                    text: 'Timestamp',
                },
                ticks: {
                    // Automatically skip labels to prevent them from overlapping
                    autoSkip: true,
                    maxTicksLimit: 10 // Show a maximum of 10 timestamps
                },
            },
            y: {
                title: {
                    display: true,
                    text: 'Values',
                },
            },
        },
    };

    // The container div will control the size. A height is needed for maintainAspectRatio: false.
    return <div className="chart-wrapper"><Line data={data} options={options} /></div>;
};

export default SensorGraph;