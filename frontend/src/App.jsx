import React, { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import SingleTransactionForensics from './components/SingleTransactionForensics';
import BatchLedgerAudit from './components/BatchLedgerAudit';
import AblationMetrics from './components/AblationMetrics';
import { checkHealth } from './services/api';
import { Shield, ExternalLink, Terminal, Activity } from 'lucide-react';

export default function App() {
  const [activeTab, setActiveTab] = useState('single');
  const [backendStatus, setBackendStatus] = useState('CONNECTING...');
  const [healthData, setHealthData] = useState(null);

  // Poll Backend Health on Mount
  useEffect(() => {
    const fetchStatus = async () => {
      try {
        const data = await checkHealth();
        setBackendStatus(data.status || 'ONLINE');
        setHealthData(data);
      } catch (err) {
        setBackendStatus('OFFLINE');
      }
    };

    fetchStatus();
    const interval = setInterval(fetchStatus, 15000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="min-h-screen bg-[#080B10] cyber-grid flex flex-col justify-between selection:bg-[#00F5FF]/30 selection:text-[#00F5FF]">
      
      {/* Top Navigation */}
      <div>
        <Navbar
          activeTab={activeTab}
          setActiveTab={setActiveTab}
          backendStatus={backendStatus}
        />

        {/* Main Content Area */}
        <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          {activeTab === 'single' && <SingleTransactionForensics />}
          {activeTab === 'batch' && <BatchLedgerAudit />}
          {activeTab === 'ablation' && <AblationMetrics />}
        </main>
      </div>

      {/* Footer & Telemetry */}
      <footer className="border-t border-[#1E293B] bg-[#080B10]/95 py-6 mt-12 font-mono text-xs text-cyber-subtext">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col md:flex-row items-center justify-between gap-4">
          
          <div className="flex items-center space-x-2">
            <Shield className="w-4 h-4 text-[#00F5FF]" />
            <span>PROJECT DEFI-FRAUD-053 &copy; 2026</span>
            <span className="text-cyber-muted">|</span>
            <span>Department of Cybersecurity, Srinivas University</span>
          </div>

          <div className="flex items-center space-x-4">
            <span className="flex items-center gap-1.5 text-cyber-subtext">
              <Activity className="w-3.5 h-3.5 text-[#00FF9D]" />
              API: <a href="http://localhost:8000/docs" target="_blank" rel="noreferrer" className="text-[#00F5FF] hover:underline flex items-center gap-0.5">
                FastAPI Swagger <ExternalLink className="w-3 h-3" />
              </a>
            </span>

            <span className="text-cyber-muted">|</span>

            <span className="text-[#00FF9D]">
              Lagrangian Parity: <b>DI &ge; 0.80 Certified</b>
            </span>
          </div>

        </div>
      </footer>

    </div>
  );
}
