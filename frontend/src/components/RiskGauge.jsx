import React from 'react';
import { AlertTriangle, CheckCircle, Shield, Zap } from 'lucide-react';

export default function RiskGauge({ probability = 0, confidence = 0, riskTier = 'LOW', prediction = 0 }) {
  const probPct = Math.min(Math.max(probability * 100, 0), 100);
  const confPct = Math.min(Math.max(confidence * 100, 0), 100);
  const isFraud = prediction === 1;

  const getTierColor = (tier) => {
    switch (tier) {
      case 'CRITICAL':
        return 'text-[#FF2A6D] bg-[#FF2A6D]/10 border-[#FF2A6D]/40';
      case 'HIGH':
        return 'text-[#FF2A6D] bg-[#FF2A6D]/10 border-[#FF2A6D]/40';
      case 'MEDIUM':
        return 'text-[#FFB800] bg-[#FFB800]/10 border-[#FFB800]/40';
      default:
        return 'text-[#00FF9D] bg-[#00FF9D]/10 border-[#00FF9D]/40';
    }
  };

  return (
    <div className="cyber-card p-5">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-xs font-mono font-bold tracking-wider text-[#00F5FF] uppercase flex items-center gap-2">
          <Zap className="w-4 h-4 text-[#00F5FF]" />
          Probability & Certainty Telemetry
        </h3>
        <span className={`px-2.5 py-0.5 rounded text-xs font-mono font-bold border uppercase ${getTierColor(riskTier)}`}>
          {riskTier} RISK
        </span>
      </div>

      {/* Fraud Probability Progress */}
      <div className="mb-4">
        <div className="flex justify-between text-xs font-mono mb-1.5">
          <span className="text-cyber-subtext">Calibrated Fraud Probability:</span>
          <span className={`font-bold text-sm ${isFraud ? 'text-[#FF2A6D]' : 'text-[#00FF9D]'}`}>
            {probPct.toFixed(2)}%
          </span>
        </div>
        <div className="h-3 w-full bg-[#080B10] rounded-full overflow-hidden p-0.5 border border-[#1E293B]">
          <div
            className={`h-full rounded-full transition-all duration-700 ${
              isFraud
                ? 'bg-gradient-to-r from-[#FFB800] via-[#FF2A6D] to-[#FF0055] shadow-neon-crimson'
                : 'bg-gradient-to-r from-[#00F5FF] to-[#00FF9D] shadow-neon-green'
            }`}
            style={{ width: `${Math.max(probPct, 2)}%` }}
          />
        </div>
      </div>

      {/* Ensemble Confidence Certainty */}
      <div>
        <div className="flex justify-between text-xs font-mono mb-1.5">
          <span className="text-cyber-subtext">Ensemble Decision Certainty:</span>
          <span className="font-bold text-[#00F5FF] text-sm">
            {confPct.toFixed(2)}%
          </span>
        </div>
        <div className="h-2 w-full bg-[#080B10] rounded-full overflow-hidden p-0.5 border border-[#1E293B]">
          <div
            className="h-full rounded-full bg-[#00F5FF] transition-all duration-700 shadow-neon-cyan"
            style={{ width: `${Math.max(confPct, 2)}%` }}
          />
        </div>
      </div>
    </div>
  );
}
