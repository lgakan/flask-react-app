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

const ServerGraph = ({ graphData }) => {
    const data = {
        labels: graphData?.labels || [], // Labels for X-axis from props
        datasets: [
            {
                label: 'Server Usage Score',
                data: graphData?.data || [], // Data for Y-axis from props
                fill: false,
                borderColor: 'rgb(75, 192, 192)',
                tension: 0.1,
            },
        ],
    };

    return <div style={{ width: '600px', margin: '50px auto' }}><Line data={data} /></div>;
};

export default ServerGraph;