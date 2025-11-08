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

    // Format the timestamp to show time, date, and year for better readability
    const formattedLabels = dataPoints.map(d => {
        const date = new Date(d.timestamp);
        // Using options for toLocaleString gives us a nice, readable format
        // e.g., "21/10/2023, 14:35"
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
                label: 'Pressure',
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
        onClick: handleChartClick,
        scales: {
            x: {
                title: {
                    display: true,
                    text: 'Timestamp',
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

    return <div style={{ width: '600px', margin: '50px auto' }}><Line data={data} options={options} /></div>;
};

export default SensorGraph;