import React, { useEffect, useState } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, BarChart, Bar } from 'recharts';
import { AlertCircle, Shield, Activity, Lock } from 'lucide-react';

interface Log {
    id: number;
    timestamp: string;
    source_ip: string;
    destination_ip: string;
    protocol: string;
    bytes_transferred: number;
    event_type: string;
    details: string;
}

const Dashboard = () => {
    const [logs, setLogs] = useState<Log[]>([]);
    const [stats, setStats] = useState({ total: 0, threats: 0, active_anomalies: 0 });

    useEffect(() => {
        const fetchLogs = async () => {
            try {
                const response = await fetch('http://localhost:8000/logs/');
                const data = await response.json();
                setLogs(data);

                // Calculate stats
                const threats = data.filter((l: Log) => l.event_type !== 'Normal').length;
                setStats({
                    total: data.length,
                    threats: threats,
                    active_anomalies: data.filter((l: Log) => l.event_type === 'Malware Detected' || l.event_type === 'DoS').length
                });
            } catch (error) {
                console.error('Error fetching logs:', error);
            }
        };

        fetchLogs();
        const interval = setInterval(fetchLogs, 2000); // Poll every 2 seconds
        return () => clearInterval(interval);
    }, []);

    const chartData = logs.slice(0, 20).reverse().map(log => ({
        time: new Date(log.timestamp).toLocaleTimeString(),
        bytes: log.bytes_transferred,
        threat: log.event_type !== 'Normal' ? 1 : 0
    }));

    return (
        <div className="p-6 bg-gray-900 min-h-screen text-white font-sans">
            <header className="mb-8 flex justify-between items-center">
                <h1 className="text-3xl font-bold flex items-center gap-2">
                    <Shield className="text-blue-500" /> AI Security Monitor
                </h1>
                <div className="flex gap-4">
                    <div className="bg-gray-800 p-4 rounded-lg flex items-center gap-3">
                        <Activity className="text-green-400" />
                        <div>
                            <p className="text-gray-400 text-sm">Total Traffic</p>
                            <p className="text-2xl font-bold">{stats.total}</p>
                        </div>
                    </div>
                    <div className="bg-gray-800 p-4 rounded-lg flex items-center gap-3">
                        <AlertCircle className="text-red-500" />
                        <div>
                            <p className="text-gray-400 text-sm">Threats Detected</p>
                            <p className="text-2xl font-bold">{stats.threats}</p>
                        </div>
                    </div>
                </div>
            </header>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {/* Network Traffic Chart */}
                <div className="bg-gray-800 p-6 rounded-lg shadow-lg">
                    <h2 className="text-xl font-semibold mb-4">Network Traffic (Bytes)</h2>
                    <div className="h-64">
                        <ResponsiveContainer width="100%" height="100%">
                            <LineChart data={chartData}>
                                <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                                <XAxis dataKey="time" stroke="#9CA3AF" />
                                <YAxis stroke="#9CA3AF" />
                                <Tooltip contentStyle={{ backgroundColor: '#1F2937', border: 'none' }} />
                                <Line type="monotone" dataKey="bytes" stroke="#3B82F6" strokeWidth={2} dot={false} />
                            </LineChart>
                        </ResponsiveContainer>
                    </div>
                </div>

                {/* Recent Logs */}
                <div className="bg-gray-800 p-6 rounded-lg shadow-lg overflow-hidden">
                    <h2 className="text-xl font-semibold mb-4">Recent Alerts</h2>
                    <div className="overflow-y-auto h-64">
                        <table className="w-full text-left">
                            <thead>
                                <tr className="text-gray-400 border-b border-gray-700">
                                    <th className="pb-2">Time</th>
                                    <th className="pb-2">Event</th>
                                    <th className="pb-2">Source IP</th>
                                    <th className="pb-2">Status</th>
                                </tr>
                            </thead>
                            <tbody>
                                {logs.slice(0, 10).map((log) => (
                                    <tr key={log.id} className="border-b border-gray-700/50 hover:bg-gray-700/30">
                                        <td className="py-2 text-sm text-gray-300">{new Date(log.timestamp).toLocaleTimeString()}</td>
                                        <td className="py-2 text-sm font-medium">{log.event_type}</td>
                                        <td className="py-2 text-sm text-gray-300">{log.source_ip}</td>
                                        <td className="py-2">
                                            <span className={`px-2 py-1 rounded text-xs ${log.event_type === 'Normal' ? 'bg-green-900 text-green-300' : 'bg-red-900 text-red-300'
                                                }`}>
                                                {log.event_type === 'Normal' ? 'Safe' : 'Critical'}
                                            </span>
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Dashboard;
