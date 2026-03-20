import React, { useEffect, useState } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { AlertCircle, Shield, Activity } from 'lucide-react';
import dynamic from 'next/dynamic';

const ThreatGlobe = dynamic(() => import('./ThreatGlobe'), { ssr: false });

// Fix #1: Use environment variable for API URL instead of hardcoded localhost
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

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
                const response = await fetch(`${API_URL}/logs/`);
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
            {/* Glass-morphism container */}
            <div className="bg-white/5 rounded-xl border border-white/10 shadow-xl p-6 backdrop-blur-sm">
                {/* Header */}
                <header className="mb-8 flex justify-between items-center">
                    <h1 className="text-3xl font-bold flex items-center gap-2">
                        <Shield className="text-cyan-400" />
                        AI Security Monitor
                    </h1>
                    <div className="flex gap-6">
                        <div className="text-center">
                            <p className="text-xs text-gray-400">Total Traffic</p>
                            <p className="text-2xl font-bold text-cyan-400">{stats.total}</p>
                        </div>
                        <div className="text-center">
                            <p className="text-xs text-gray-400">Threats Detected</p>
                            <p className="text-2xl font-bold text-red-400">{stats.threats}</p>
                        </div>
                        <div className="text-center">
                            <p className="text-xs text-gray-400">Active Anomalies</p>
                            <p className="text-2xl font-bold text-yellow-400">{stats.active_anomalies}</p>
                        </div>
                    </div>
                </header>

                {/* Main Grid */}
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
                    {/* 3D Threat Globe */}
                    <div className="bg-white/5 rounded-xl border border-white/10 p-4">
                        <h2 className="text-lg font-semibold mb-3 flex items-center gap-2">
                            <Activity className="text-cyan-400" size={18} />
                            Global Threat Landscape
                        </h2>
                        <ThreatGlobe />
                    </div>

                    {/* Network Traffic Chart */}
                    <div className="bg-white/5 rounded-xl border border-white/10 p-4">
                        <h2 className="text-lg font-semibold mb-3">Network Traffic (Bytes)</h2>
                        <ResponsiveContainer width="100%" height={250}>
                            <LineChart data={chartData}>
                                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
                                <XAxis dataKey="time" tick={{ fontSize: 10, fill: '#9ca3af' }} />
                                <YAxis tick={{ fontSize: 10, fill: '#9ca3af' }} />
                                <Tooltip
                                    contentStyle={{ backgroundColor: '#1f2937', border: '1px solid rgba(255,255,255,0.1)' }}
                                />
                                <Line type="monotone" dataKey="bytes" stroke="#22d3ee" strokeWidth={2} dot={false} />
                                <Line type="monotone" dataKey="threat" stroke="#f87171" strokeWidth={2} dot={false} />
                            </LineChart>
                        </ResponsiveContainer>
                    </div>
                </div>

                {/* Recent Alerts */}
                <div className="bg-white/5 rounded-xl border border-white/10 p-4">
                    <h2 className="text-lg font-semibold mb-3 flex items-center gap-2">
                        <AlertCircle className="text-red-400" size={18} />
                        Recent Alerts
                    </h2>
                    <div className="overflow-x-auto">
                        <table className="w-full text-sm">
                            <thead>
                                <tr className="text-gray-400 border-b border-white/10">
                                    <th className="text-left pb-2">Time</th>
                                    <th className="text-left pb-2">Event</th>
                                    <th className="text-left pb-2">Source IP</th>
                                    <th className="text-left pb-2">Status</th>
                                </tr>
                            </thead>
                            <tbody>
                                {logs.slice(0, 10).map(log => (
                                    <tr key={log.id} className="border-b border-white/5 hover:bg-white/5">
                                        <td className="py-2">{new Date(log.timestamp).toLocaleTimeString()}</td>
                                        <td className="py-2">{log.event_type}</td>
                                        <td className="py-2">{log.source_ip}</td>
                                        <td className="py-2">
                                            <span className={`px-2 py-1 rounded text-xs font-medium ${
                                                log.event_type === 'Normal'
                                                    ? 'bg-green-500/20 text-green-400'
                                                    : 'bg-red-500/20 text-red-400'
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
