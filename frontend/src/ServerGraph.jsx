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

const ServerGraph = ({ dataPoints, onPointClick }) => {
    const handleChartClick = (event, elements) => {
        if (elements.length > 0) {
            const dataIndex = elements[0].index;
            onPointClick(dataPoints[dataIndex]);
        }
    };
    // Format the timestamp for better readability on the X-axis
    const formattedLabels = dataPoints.map(d => new Date(d.timestamp).toLocaleTimeString());

    const data = {
        labels: formattedLabels,
        datasets: [
            {
                label: 'CPU Usage (%)',
                data: dataPoints.map(d => d.cpuUsage),
                fill: false,
                borderColor: 'rgb(75, 192, 192)', // A nice teal color
                tension: 0.1,
            },
            {
                label: 'Memory Usage (%)',
                data: dataPoints.map(d => d.memoryUsage),
                fill: false,
                borderColor: 'rgb(255, 99, 132)', // A nice red color
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
                    text: 'Values (%)',
                },
            },
        },
    };

    return <div style={{ width: '600px', margin: '50px auto' }}><Line data={data} options={options} /></div>;
};

export default ServerGraph;