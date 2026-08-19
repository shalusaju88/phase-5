import React from 'react';
import { Shield, ShieldAlert, Cpu, Activity, Scale, Terminal } from 'lucide-react';

export default function Navbar({ activeTab, setActiveTab, backendStatus }) {
  const isHealthy = backendStatus === 'ONLINE' || backendStatus === 'HEALTHY';

  return (
    <header className="border-b border-[#1E293B] bg-[#080B10]/90 backdrop-blur-md sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-20">
          
          {/* Logo & Title */}
          <div className="flex items-center space-x-4">
            <div className="relative flex items-center justify-center w-12 h-12 rounded-xl bg-gradient-to-br from-[#00F5FF]/20 to-[#00FF9D]/10 border border-[#00F5FF]/40 shadow-neon-cyan">
              <Shield className="w-6 h-6 text-[#00F5FF]" />
              <div className="absolute -top-1 -right-1 w-3 h-3 bg-[#00FF9D] rounded-full animate-ping"></div>
              <div className="absolute -top-1 -right-1 w-3 h-3 bg-[#00FF9D] rounded-full"></div>
            </div>
            <div>
              <div className="flex items-center space-x-2">
                <span className="font-mono text-xs font-bold uppercase tracking-widest text-[#00F5FF] bg-[#00F5FF]/10 px-2 py-0.5 rounded border border-[#00F5FF]/30">
                  DEFI-FRAUD-053
                </span>
                <span className="text-xs text-cyber-muted font-mono">IEEE TIFS 2026</span>
              </div>
              <h1 className="text-lg sm:text-xl font-bold tracking-tight text-white font-sans flex items-center gap-2">
                Forensic Intelligence Matrix
                <span className="text-xs font-normal px-2 py-0.5 rounded-full bg-[#00FF9D]/10 text-[#00FF9D] border border-[#00FF9D]/30">
                  Champion Model A
                </span>
              </h1>
            </div>
          </div>

          {/* System Telemetry Badges */}
          <div className="hidden lg:flex items-center space-x-3">
            <div className="flex items-center space-x-2 px-3 py-1.5 rounded-lg bg-[#0F172A] border border-[#1E293B] font-mono text-xs">
              <Scale className="w-3.5 h-3.5 text-[#00F5FF]" />
              <span className="text-cyber-subtext">Lagrangian Fairness:</span>
              <span className="text-[#00FF9D] font-bold">DI &ge; 0.80</span>
            </div>

            <div className="flex items-center space-x-2 px-3 py-1.5 rounded-lg bg-[#0F172A] border border-[#1E293B] font-mono text-xs">
              <Cpu className="w-3.5 h-3.5 text-[#FFB800]" />
              <span className="text-cyber-subtext">Ensemble:</span>
              <span className="text-[#F8FAFC]">4-Tree Stack + UMAP</span>
            </div>

            <div className="flex items-center space-x-2 px-3 py-1.5 rounded-lg bg-[#0F172A] border border-[#1E293B] font-mono text-xs">
              <Activity className={`w-3.5 h-3.5 ${isHealthy ? 'text-[#00FF9D] animate-pulse' : 'text-[#FF2A6D]'}`} />
              <span className="text-cyber-subtext">Backend:</span>
              <span className={`font-bold ${isHealthy ? 'text-[#00FF9D]' : 'text-[#FF2A6D]'}`}>
                {backendStatus || 'CONNECTING...'}
              </span>
            </div>
          </div>

        </div>

        {/* Tab Navigation */}
        <div className="flex space-x-2 border-t border-[#1E293B]/60 pt-2 pb-3 overflow-x-auto">
          <button
            onClick={() => setActiveTab('single')}
            className={`flex items-center space-x-2 px-4 py-2 rounded-lg font-mono text-xs sm:text-sm font-semibold transition-all whitespace-nowrap ${
              activeTab === 'single'
                ? 'bg-gradient-to-r from-[#00F5FF]/20 to-[#00B4D8]/10 text-[#00F5FF] border border-[#00F5FF]/50 shadow-neon-cyan'
                : 'text-cyber-subtext hover:text-white hover:bg-[#111C33]/60'
            }`}
          >
            <Terminal className="w-4 h-4" />
            <span>1. SINGLE TRANSACTION FORENSICS</span>
          </button>

          <button
            onClick={() => setActiveTab('batch')}
            className={`flex items-center space-x-2 px-4 py-2 rounded-lg font-mono text-xs sm:text-sm font-semibold transition-all whitespace-nowrap ${
              activeTab === 'batch'
                ? 'bg-gradient-to-r from-[#00F5FF]/20 to-[#00B4D8]/10 text-[#00F5FF] border border-[#00F5FF]/50 shadow-neon-cyan'
                : 'text-cyber-subtext hover:text-white hover:bg-[#111C33]/60'
            }`}
          >
            <ShieldAlert className="w-4 h-4" />
            <span>2. BATCH LEDGER AUDIT</span>
          </button>

          <button
            onClick={() => setActiveTab('ablation')}
            className={`flex items-center space-x-2 px-4 py-2 rounded-lg font-mono text-xs sm:text-sm font-semibold transition-all whitespace-nowrap ${
              activeTab === 'ablation'
                ? 'bg-gradient-to-r from-[#00F5FF]/20 to-[#00B4D8]/10 text-[#00F5FF] border border-[#00F5FF]/50 shadow-neon-cyan'
                : 'text-cyber-subtext hover:text-white hover:bg-[#111C33]/60'
            }`}
          >
            <Cpu className="w-4 h-4" />
            <span>3. IEEE TIFS ABLATION BENCHMARK</span>
          </button>
        </div>

      </div>
    </header>
  );
}
