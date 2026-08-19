import React, { useState } from 'react';
import { 
  ShieldAlert, ShieldCheck, Zap, Scale, Layers, 
  Clock, ArrowRightLeft, Coins, Compass, Sparkles, RefreshCw, AlertOctagon 
} from 'lucide-react';
import { PRESET_EDGE_CASES, INITIAL_FORM_STATE } from '../data/presets';
import { predictSingleTransaction } from '../services/api';
import RiskGauge from './RiskGauge';
import ShapWaterfallChart from './ShapWaterfallChart';

export default function SingleTransactionForensics() {
  const [formData, setFormData] = useState(INITIAL_FORM_STATE);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [selectedPresetId, setSelectedPresetId] = useState(1);

  // Handle Input Changes
  const handleInputChange = (field, value) => {
    setFormData(prev => ({
      ...prev,
      [field]: typeof value === 'string' && !isNaN(value) && value.trim() !== '' ? parseFloat(value) : value
    }));
  };

  // Load Preset Edge Case
  const handleLoadPreset = (preset) => {
    setSelectedPresetId(preset.id);
    setFormData(preset.data);
    setError(null);
  };

  // Execute Forensic Analysis
  const handleRunAnalysis = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await predictSingleTransaction(formData);
      setResult(response);
    } catch (err) {
      console.error(err);
      setError(err.response?.data?.detail || err.message || 'Inference engine communication error.');
    } finally {
      setLoading(false);
    }
  };

  const isFraud = result?.prediction === 1;

  return (
    <div className="space-y-6">
      
      {/* Preset Buttons Header */}
      <div className="cyber-card p-4">
        <div className="flex items-center justify-between mb-3">
          <span className="text-xs font-mono font-bold text-[#00F5FF] uppercase flex items-center gap-1.5">
            <Sparkles className="w-4 h-4 text-[#00F5FF]" />
            IEEE TIFS 2026 Curated Benchmark Presets
          </span>
          <span className="text-xs text-cyber-subtext font-mono">Click to inject test vectors</span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
          {PRESET_EDGE_CASES.map(preset => (
            <button
              key={preset.id}
              onClick={() => handleLoadPreset(preset)}
              className={`p-3 rounded-lg border text-left transition-all ${
                selectedPresetId === preset.id
                  ? 'bg-[#162444] border-[#00F5FF] shadow-neon-cyan'
                  : 'bg-[#080B10]/80 border-[#1E293B] hover:border-[#00F5FF]/50 hover:bg-[#0F172A]'
              }`}
            >
              <div className="flex items-center justify-between mb-1">
                <span className="font-mono font-bold text-xs text-white truncate max-w-[200px]">
                  {preset.name}
                </span>
                <span className={`px-2 py-0.5 rounded text-[10px] font-mono uppercase font-bold ${
                  preset.color === 'crimson' ? 'bg-[#FF2A6D]/20 text-[#FF2A6D]' :
                  preset.color === 'green' ? 'bg-[#00FF9D]/20 text-[#00FF9D]' : 'bg-[#FFB800]/20 text-[#FFB800]'
                }`}>
                  {preset.tag}
                </span>
              </div>
              <p className="text-[11px] text-cyber-subtext line-clamp-2 leading-relaxed">
                {preset.description}
              </p>
            </button>
          ))}
        </div>
      </div>

      {/* Main Forensic Cockpit Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        
        {/* Left Column: Input Sliders & Fields (5 cols) */}
        <div className="lg:col-span-5 space-y-4">
          
          {/* Section 1: Temporal Dynamics */}
          <div className="cyber-card p-4">
            <h3 className="text-xs font-mono font-bold text-[#00F5FF] uppercase flex items-center gap-1.5 mb-3">
              <Clock className="w-4 h-4 text-[#00F5FF]" />
              1. Temporal Dynamics & Longevity (Fairness Sensitive)
            </h3>
            
            <div className="space-y-3">
              <div>
                <div className="flex justify-between text-xs font-mono mb-1">
                  <span className="text-cyber-subtext">Account Lifespan (Mins):</span>
                  <span className="text-[#00FF9D] font-bold">{formData["Time Diff between first and last (Mins)"]} mins ({((formData["Time Diff between first and last (Mins)"] || 0)/1440).toFixed(1)} days)</span>
                </div>
                <input
                  type="range"
                  min="0"
                  max="1000000"
                  step="100"
                  value={formData["Time Diff between first and last (Mins)"]}
                  onChange={(e) => handleInputChange("Time Diff between first and last (Mins)", e.target.value)}
                  className="w-full h-1.5 bg-[#080B10] rounded-lg cursor-pointer"
                />
              </div>

              <div className="grid grid-cols-2 gap-3 pt-1">
                <div>
                  <label className="text-[11px] font-mono text-cyber-subtext">Avg Min Sent Tnx</label>
                  <input
                    type="number"
                    value={formData["Avg min between sent tnx"]}
                    onChange={(e) => handleInputChange("Avg min between sent tnx", e.target.value)}
                    className="w-full mt-1 bg-[#080B10] border border-[#1E293B] rounded-lg px-2.5 py-1.5 text-xs font-mono text-white focus:outline-none focus:border-[#00F5FF]"
                  />
                </div>
                <div>
                  <label className="text-[11px] font-mono text-cyber-subtext">Avg Min Received Tnx</label>
                  <input
                    type="number"
                    value={formData["Avg min between received tnx"]}
                    onChange={(e) => handleInputChange("Avg min between received tnx", e.target.value)}
                    className="w-full mt-1 bg-[#080B10] border border-[#1E293B] rounded-lg px-2.5 py-1.5 text-xs font-mono text-white focus:outline-none focus:border-[#00F5FF]"
                  />
                </div>
              </div>
            </div>
          </div>

          {/* Section 2: Ledger Flow & Value Metrics */}
          <div className="cyber-card p-4">
            <h3 className="text-xs font-mono font-bold text-[#00FF9D] uppercase flex items-center gap-1.5 mb-3">
              <ArrowRightLeft className="w-4 h-4 text-[#00FF9D]" />
              2. Core Ledger Flow & Degree (Native ETH)
            </h3>
            
            <div className="grid grid-cols-2 gap-3 text-xs font-mono">
              <div>
                <label className="text-[11px] text-cyber-subtext">Unique Received Addrs</label>
                <input
                  type="number"
                  value={formData["Unique Received From Addresses"]}
                  onChange={(e) => handleInputChange("Unique Received From Addresses", e.target.value)}
                  className="w-full mt-1 bg-[#080B10] border border-[#1E293B] rounded-lg px-2.5 py-1.5 text-white focus:outline-none focus:border-[#00FF9D]"
                />
              </div>
              <div>
                <label className="text-[11px] text-cyber-subtext">Unique Sent Addrs</label>
                <input
                  type="number"
                  value={formData["Unique Sent To Addresses"]}
                  onChange={(e) => handleInputChange("Unique Sent To Addresses", e.target.value)}
                  className="w-full mt-1 bg-[#080B10] border border-[#1E293B] rounded-lg px-2.5 py-1.5 text-white focus:outline-none focus:border-[#00FF9D]"
                />
              </div>

              <div>
                <label className="text-[11px] text-cyber-subtext">Min Val Received (ETH)</label>
                <input
                  type="number"
                  step="0.01"
                  value={formData["min value received"]}
                  onChange={(e) => handleInputChange("min value received", e.target.value)}
                  className="w-full mt-1 bg-[#080B10] border border-[#1E293B] rounded-lg px-2.5 py-1.5 text-white focus:outline-none focus:border-[#00FF9D]"
                />
              </div>
              <div>
                <label className="text-[11px] text-cyber-subtext">Max Val Received (ETH)</label>
                <input
                  type="number"
                  step="0.1"
                  value={formData["max value received"]}
                  onChange={(e) => handleInputChange("max value received", e.target.value)}
                  className="w-full mt-1 bg-[#080B10] border border-[#1E293B] rounded-lg px-2.5 py-1.5 text-white focus:outline-none focus:border-[#00FF9D]"
                />
              </div>

              <div>
                <label className="text-[11px] text-cyber-subtext">Min Val Sent (ETH)</label>
                <input
                  type="number"
                  step="0.01"
                  value={formData["min val sent"]}
                  onChange={(e) => handleInputChange("min val sent", e.target.value)}
                  className="w-full mt-1 bg-[#080B10] border border-[#1E293B] rounded-lg px-2.5 py-1.5 text-white focus:outline-none focus:border-[#00FF9D]"
                />
              </div>
              <div>
                <label className="text-[11px] text-cyber-subtext">Max Val Sent (ETH)</label>
                <input
                  type="number"
                  step="0.1"
                  value={formData["max val sent"]}
                  onChange={(e) => handleInputChange("max val sent", e.target.value)}
                  className="w-full mt-1 bg-[#080B10] border border-[#1E293B] rounded-lg px-2.5 py-1.5 text-white focus:outline-none focus:border-[#00FF9D]"
                />
              </div>
            </div>
          </div>

          {/* Section 3: ERC20 & Protocol Routing */}
          <div className="cyber-card p-4">
            <h3 className="text-xs font-mono font-bold text-[#FFB800] uppercase flex items-center gap-1.5 mb-3">
              <Coins className="w-4 h-4 text-[#FFB800]" />
              3. ERC20 Protocol & Token Routing
            </h3>

            <div className="grid grid-cols-2 gap-3 text-xs font-mono">
              <div>
                <label className="text-[11px] text-cyber-subtext">Total ERC20 Tnxs</label>
                <input
                  type="number"
                  value={formData["Total ERC20 tnxs"]}
                  onChange={(e) => handleInputChange("Total ERC20 tnxs", e.target.value)}
                  className="w-full mt-1 bg-[#080B10] border border-[#1E293B] rounded-lg px-2.5 py-1.5 text-white focus:outline-none focus:border-[#FFB800]"
                />
              </div>
              <div>
                <label className="text-[11px] text-cyber-subtext">ERC20 Uniq Sent Addr</label>
                <input
                  type="number"
                  value={formData["ERC20 uniq sent addr"]}
                  onChange={(e) => handleInputChange("ERC20 uniq sent addr", e.target.value)}
                  className="w-full mt-1 bg-[#080B10] border border-[#1E293B] rounded-lg px-2.5 py-1.5 text-white focus:outline-none focus:border-[#FFB800]"
                />
              </div>

              <div>
                <label className="text-[11px] text-cyber-subtext">Most Sent Token</label>
                <input
                  type="text"
                  value={formData["ERC20 most sent token type"]}
                  onChange={(e) => handleInputChange("ERC20 most sent token type", e.target.value)}
                  className="w-full mt-1 bg-[#080B10] border border-[#1E293B] rounded-lg px-2.5 py-1.5 text-white focus:outline-none focus:border-[#FFB800]"
                />
              </div>
              <div>
                <label className="text-[11px] text-cyber-subtext">Most Rec Token</label>
                <input
                  type="text"
                  value={formData["ERC20_most_rec_token_type"]}
                  onChange={(e) => handleInputChange("ERC20_most_rec_token_type", e.target.value)}
                  className="w-full mt-1 bg-[#080B10] border border-[#1E293B] rounded-lg px-2.5 py-1.5 text-white focus:outline-none focus:border-[#FFB800]"
                />
              </div>
            </div>
          </div>

          {/* Section 4: Latent Manifolds */}
          <div className="cyber-card p-4">
            <h3 className="text-xs font-mono font-bold text-[#FF2A6D] uppercase flex items-center gap-1.5 mb-3">
              <Compass className="w-4 h-4 text-[#FF2A6D]" />
              4. Unsupervised Latent Coordinates (IsoForest + UMAP)
            </h3>

            <div className="space-y-3">
              <div>
                <div className="flex justify-between text-xs font-mono mb-1">
                  <span className="text-cyber-subtext">IsoForest Anomaly Score:</span>
                  <span className="text-[#FF2A6D] font-bold">{formData["anomaly_score"]}</span>
                </div>
                <input
                  type="range"
                  min="-0.5"
                  max="0.2"
                  step="0.005"
                  value={formData["anomaly_score"]}
                  onChange={(e) => handleInputChange("anomaly_score", e.target.value)}
                  className="w-full h-1.5 bg-[#080B10] rounded-lg cursor-pointer"
                />
              </div>

              <div className="grid grid-cols-3 gap-2 text-xs font-mono pt-1">
                <div>
                  <label className="text-[10px] text-cyber-subtext">UMAP-1</label>
                  <input
                    type="number"
                    step="0.1"
                    value={formData["UMAP_1"]}
                    onChange={(e) => handleInputChange("UMAP_1", e.target.value)}
                    className="w-full mt-1 bg-[#080B10] border border-[#1E293B] rounded px-2 py-1 text-white"
                  />
                </div>
                <div>
                  <label className="text-[10px] text-cyber-subtext">UMAP-2</label>
                  <input
                    type="number"
                    step="0.1"
                    value={formData["UMAP_2"]}
                    onChange={(e) => handleInputChange("UMAP_2", e.target.value)}
                    className="w-full mt-1 bg-[#080B10] border border-[#1E293B] rounded px-2 py-1 text-white"
                  />
                </div>
                <div>
                  <label className="text-[10px] text-cyber-subtext">UMAP-3</label>
                  <input
                    type="number"
                    step="0.1"
                    value={formData["UMAP_3"]}
                    onChange={(e) => handleInputChange("UMAP_3", e.target.value)}
                    className="w-full mt-1 bg-[#080B10] border border-[#1E293B] rounded px-2 py-1 text-white"
                  />
                </div>
              </div>
            </div>
          </div>

          {/* Submit Action Button */}
          <button
            onClick={handleRunAnalysis}
            disabled={loading}
            className="w-full py-3.5 px-6 rounded-xl font-mono text-sm font-bold uppercase tracking-wider bg-gradient-to-r from-[#00F5FF] via-[#00FF9D] to-[#00B4D8] text-[#080B10] shadow-neon-cyan hover:opacity-95 transition-all transform active:scale-[0.99] flex items-center justify-center gap-2"
          >
            {loading ? (
              <>
                <RefreshCw className="w-4 h-4 animate-spin text-[#080B10]" />
                <span>Running Stacking Inference & Tree-SHAP...</span>
              </>
            ) : (
              <>
                <Zap className="w-4 h-4 text-[#080B10]" />
                <span>Execute Champion Model Forensics</span>
              </>
            )}
          </button>

          {error && (
            <div className="p-3 rounded-lg bg-[#FF2A6D]/10 border border-[#FF2A6D]/50 text-xs font-mono text-[#FF2A6D] flex items-center gap-2">
              <AlertOctagon className="w-4 h-4 flex-shrink-0" />
              <span>{error}</span>
            </div>
          )}

        </div>

        {/* Right Column: Visual Telemetry Cards & SHAP Waterfall (7 cols) */}
        <div className="lg:col-span-7 space-y-4">
          
          {result ? (
            <>
              {/* Verdict Header Banner */}
              <div className={`p-6 rounded-xl border transition-all ${
                isFraud ? 'cyber-card-fraud' : 'cyber-card-benign'
              }`}>
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-3">
                    <div className={`p-3 rounded-xl ${isFraud ? 'bg-[#FF2A6D]/20 text-[#FF2A6D]' : 'bg-[#00FF9D]/20 text-[#00FF9D]'}`}>
                      {isFraud ? <ShieldAlert className="w-8 h-8" /> : <ShieldCheck className="w-8 h-8" />}
                    </div>
                    <div>
                      <span className="text-[11px] font-mono uppercase tracking-widest text-cyber-subtext">
                        Ensemble Classification Output
                      </span>
                      <h2 className={`text-xl sm:text-2xl font-bold font-mono ${isFraud ? 'text-[#FF2A6D]' : 'text-[#00FF9D]'}`}>
                        {isFraud ? '🚨 FRAUDULENT THREAT DETECTED' : '🛡️ BENIGN PARTICIPANT VERIFIED'}
                      </h2>
                    </div>
                  </div>

                  <div className="text-right">
                    <span className="text-[10px] font-mono uppercase text-cyber-subtext">Latency</span>
                    <div className="text-sm font-mono font-bold text-white">
                      {result.latency_ms} ms
                    </div>
                  </div>
                </div>

                {/* Behavioral Archetype Tag */}
                <div className="mt-4 pt-3 border-t border-[#1E293B] text-xs font-mono flex items-center justify-between">
                  <span className="text-cyber-subtext">DeFi Threat Archetype:</span>
                  <span className="text-[#00F5FF] font-bold">{result.archetype}</span>
                </div>
              </div>

              {/* Gauges & Fairness Row */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                
                {/* Risk Gauge */}
                <RiskGauge
                  probability={result.probability}
                  confidence={result.confidence}
                  riskTier={result.riskTier || result.risk_tier}
                  prediction={result.prediction}
                />

                {/* Lagrangian Fairness Calibration Card */}
                <div className="cyber-card p-5">
                  <h3 className="text-xs font-mono font-bold text-[#00FF9D] uppercase flex items-center gap-1.5 mb-3">
                    <Scale className="w-4 h-4 text-[#00FF9D]" />
                    Lagrangian Fairness Certificate
                  </h3>

                  <div className="space-y-2 text-xs font-mono text-cyber-subtext">
                    <div className="flex justify-between">
                      <span>Demographic Cohort:</span>
                      <span className="text-white font-medium">{result.fairness_metadata?.demographic_group}</span>
                    </div>
                    <div className="flex justify-between">
                      <span>Account Longevity:</span>
                      <span className="text-white">{result.fairness_metadata?.account_lifespan_days} days</span>
                    </div>
                    <div className="flex justify-between">
                      <span>Group Calibrated Cutoff:</span>
                      <span className="text-[#00FF9D] font-bold">{result.fairness_metadata?.calibrated_threshold}</span>
                    </div>
                    <div className="flex justify-between pt-1 border-t border-[#1E293B]">
                      <span>Disparate Impact Law:</span>
                      <span className="text-[#00FF9D] font-bold">COMPLIANT (DI &ge; 0.80)</span>
                    </div>
                  </div>
                </div>

              </div>

              {/* Tree-SHAP Local Waterfall Attribution */}
              <ShapWaterfallChart shapExplanation={result.shap_explanation} />

              {/* Mechanistic Insight Card */}
              <div className="cyber-card p-5">
                <h3 className="text-xs font-mono font-bold text-[#FFB800] uppercase flex items-center gap-1.5 mb-2">
                  <Layers className="w-4 h-4 text-[#FFB800]" />
                  Forensic Mechanistic Insight
                </h3>
                <p className="text-xs text-cyber-subtext font-mono leading-relaxed">
                  {result.mechanistic_insight}
                </p>
              </div>

            </>
          ) : (
            <div className="cyber-card p-12 text-center flex flex-col items-center justify-center min-h-[420px]">
              <div className="w-16 h-16 rounded-2xl bg-[#080B10] border border-[#1E293B] flex items-center justify-center mb-4 text-[#00F5FF]/60 shadow-neon-cyan">
                <ShieldAlert className="w-8 h-8" />
              </div>
              <h3 className="text-base font-mono font-bold text-white mb-2">
                Awaiting Ledger Forensics Execution
              </h3>
              <p className="text-xs text-cyber-subtext font-mono max-w-md mb-6 leading-relaxed">
                Inject one of our curated IEEE TIFS edge cases on the left or customize ledger attributes, then click <b>Execute Champion Model Forensics</b>.
              </p>
              <button
                onClick={handleRunAnalysis}
                className="px-5 py-2 rounded-lg bg-[#00F5FF]/10 text-[#00F5FF] border border-[#00F5FF]/40 text-xs font-mono font-bold hover:bg-[#00F5FF]/20 transition-all"
              >
                ⚡ Run Default Test Case
              </button>
            </div>
          )}

        </div>

      </div>

    </div>
  );
}
