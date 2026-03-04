import React, { useEffect, useState } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { AlertCircle, Shield, Activity } from 'lucide-react';
import dynamic from 'next/dynamic';

const ThreatGlobe = dynamic(() => import('./ThreatGlobe'), { ssr: false });

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

const Dashboard: React.FC = () => {
    const [logs, setLogs] = useState<Log[]>([]);
    const [stats, setStats] = useState({ total: 0, threats: 0, active_anomalies: 0 });

    useEffect(() => {
        const fetchLogs = async () => {
            try {
                const response = await fetch('http://localhost:8000/logs/');
                const data: Log[] = await response.json();
                setLogs(data);
                const threats = data.filter(l => l.event_type !== 'Normal').length;
                const active = data.filter(l => l.event_type === 'Malware Detected' || l.event_type === 'DoS').length;
                setStats({ total: data.length, threats, active_anomalies: active });
            } catch (error) {
                console.error('Error fetching logs:', error);
            }
        };
        fetchLogs();
        const interval = setInterval(fetchLogs, 2000);
        return () => clearInterval(interval);
    }, []);

    const chartData = logs.slice(0, 20).reverse().map(log => ({
        time: new Date(log.timestamp).toLocaleTimeString(),
        bytes: log.bytes_transferred,
        threat: log.event_type !== 'Normal' ? 1 : 0,
    }));

    return (
        <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-gray-700 text-white font-sans p-6 backdrop-blur-sm">
            {/* Glass‑morphism container */}
            <div className="bg-white/5 rounded-xl border border-white/10 shadow-xl p-6 backdrop-blur-sm">
                {/* Header */}
                <header className="mb-8 flex justify-between items-center">
                    <h1 className="text-3xl font-bold flex items-center gap-2">
                        <Shield className="text-blue-400" /> AI Security Monitor
                    </h1>
                    <div className="flex gap-4">
                        <div className="bg-white/10 p-4 rounded-lg flex items-center gap-3">
                            <Activity className="text-green-400" />
                            <div>
                                <p className="text-gray-300 text-sm">Total Traffic</p>
                                <p className="text-2xl font-bold">{stats.total}</p>
                            </div>
                        </div>
                        <div className="bg-white/10 p-4 rounded-lg flex items-center gap-3">
                            <AlertCircle className="text-red-400" />
                            <div>
                                <p className="text-gray-300 text-sm">Threats Detected</p>
                                <p className="text-2xl font-bold">{stats.threats}</p>
                            </div>
                        </div>
                    </div>
                </header>

                {/* Main Grid */}
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                    {/* 3D Threat Globe */}
                    <div className="bg-white/5 rounded-xl border border-white/10 shadow-xl p-4 backdrop-blur-sm">
                        <h2 className="text-xl font-semibold mb-2 text-gray-200">Global Threat Landscape</h2>
                        <ThreatGlobe />
                    </div>
                    {/* Network Traffic Chart */}
                    <div className="bg-white/5 rounded-xl border border-white/10 shadow-xl p-4 backdrop-blur-sm">
                        <h2 className="text-xl font-semibold mb-4 text-gray-200">Network Traffic (Bytes)</h2>
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
                </div>

                {/* Recent Alerts */}
                <div className="mt-8 bg-gray-800 p-6 rounded-lg shadow-lg overflow-hidden">
                    <h2 className="text-xl font-semibold mb-4 text-gray-200">Recent Alerts</h2>
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
                                {logs.slice(0, 10).map(log => (
                                    <tr key={log.id} className="border-b border-gray-700/50 hover:bg-gray-700/30">
                                        <td className="py-2 text-sm text-gray-300">{new Date(log.timestamp).toLocaleTimeString()}</td>
                                        <td className="py-2 text-sm font-medium">{log.event_type}</td>
                                        <td className="py-2 text-sm text-gray-300">{log.source_ip}</td>
                                        <td className="py-2">
                                            <span className={`px-2 py-1 rounded text-xs ${log.event_type === 'Normal' ? 'bg-green-900 text-green-300' : 'bg-red-900 text-red-300'}`}>
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
