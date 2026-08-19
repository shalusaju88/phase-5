import React from 'react';
import { BarChart3, TrendingUp, TrendingDown, Info } from 'lucide-react';

export default function ShapWaterfallChart({ shapExplanation }) {
  if (!shapExplanation || !shapExplanation.feature_attributions) {
    return (
      <div className="cyber-card p-6 text-center text-cyber-muted font-mono text-xs">
        Awaiting transaction payload to compute Tree-SHAP attribution vector...
      </div>
    );
  }

  const { feature_attributions, top_risk_drivers, top_mitigating_factors, base_value } = shapExplanation;

  // Sort by absolute Shapley magnitude
  const sortedFeatures = Object.entries(feature_attributions)
    .map(([feature, value]) => ({ feature, value }))
    .sort((a, b) => Math.abs(b.value) - Math.abs(a.value))
    .slice(0, 10);

  const maxAbsVal = Math.max(...sortedFeatures.map(f => Math.abs(f.value)), 0.1);

  return (
    <div className="cyber-card p-5">
      
      {/* Header */}
      <div className="flex items-center justify-between mb-4">
        <div>
          <h3 className="text-xs font-mono font-bold tracking-wider text-[#00FF9D] uppercase flex items-center gap-2">
            <BarChart3 className="w-4 h-4 text-[#00FF9D]" />
            Local Tree-SHAP Attribution Waterfall (Instance Proof)
          </h3>
          <p className="text-xs text-cyber-subtext font-mono mt-0.5">
            Base Log-Odds Prior: <span className="text-white font-bold">{base_value?.toFixed(4) || '0.5000'}</span>
          </p>
        </div>

        {/* Legend */}
        <div className="flex items-center space-x-3 text-[11px] font-mono">
          <span className="flex items-center gap-1 text-[#FF2A6D]">
            <span className="w-2.5 h-2.5 rounded-sm bg-[#FF2A6D]"></span> +SHAP (Fraud)
          </span>
          <span className="flex items-center gap-1 text-[#00F5FF]">
            <span className="w-2.5 h-2.5 rounded-sm bg-[#00F5FF]"></span> -SHAP (Benign)
          </span>
        </div>
      </div>

      {/* Waterfall Bars */}
      <div className="space-y-2.5 my-4">
        {sortedFeatures.map(({ feature, value }, idx) => {
          const isPositive = value >= 0;
          const widthPct = Math.min((Math.abs(value) / maxAbsVal) * 100, 100);

          return (
            <div key={idx} className="group text-xs font-mono">
              <div className="flex justify-between items-center mb-1 text-cyber-subtext group-hover:text-white transition-colors">
                <span className="truncate max-w-[280px] font-medium" title={feature}>
                  {idx + 1}. {feature}
                </span>
                <span className={`font-bold ${isPositive ? 'text-[#FF2A6D]' : 'text-[#00F5FF]'}`}>
                  {isPositive ? `+${value.toFixed(4)}` : value.toFixed(4)}
                </span>
              </div>

              {/* Bidirectional Bar */}
              <div className="h-4 w-full bg-[#080B10] rounded border border-[#1E293B] relative overflow-hidden flex items-center">
                {/* Center baseline indicator */}
                <div className="absolute left-1/2 top-0 bottom-0 w-px bg-[#334155] z-10"></div>

                {isPositive ? (
                  <div
                    className="h-full bg-gradient-to-r from-[#FF2A6D]/70 to-[#FF2A6D] rounded-r transition-all duration-500 shadow-neon-crimson"
                    style={{
                      marginLeft: '50%',
                      width: `${widthPct / 2}%`,
                    }}
                  />
                ) : (
                  <div
                    className="h-full bg-gradient-to-l from-[#00F5FF]/70 to-[#00F5FF] rounded-l transition-all duration-500 shadow-neon-cyan"
                    style={{
                      marginRight: '50%',
                      marginLeft: `${50 - widthPct / 2}%`,
                      width: `${widthPct / 2}%`,
                    }}
                  />
                )}
              </div>
            </div>
          );
        })}
      </div>

      {/* Driver Analysis Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-3 mt-5 pt-4 border-t border-[#1E293B]/70">
        
        {/* Top Risk Pushers */}
        <div className="p-3 rounded-lg bg-[#080B10] border border-[#FF2A6D]/30">
          <div className="flex items-center gap-1.5 text-xs font-mono font-bold text-[#FF2A6D] mb-2">
            <TrendingUp className="w-3.5 h-3.5" />
            Top Fraud Escalators (+SHAP)
          </div>
          <ul className="space-y-1 text-[11px] font-mono text-cyber-subtext">
            {top_risk_drivers && top_risk_drivers.length > 0 ? (
              top_risk_drivers.slice(0, 3).map((d, i) => (
                <li key={i} className="flex justify-between">
                  <span className="truncate max-w-[180px]">{d.feature}</span>
                  <span className="text-[#FF2A6D] font-bold">+{d.shap_value.toFixed(3)}</span>
                </li>
              ))
            ) : (
              <li className="text-cyber-muted">No high-risk escalators found</li>
            )}
          </ul>
        </div>

        {/* Top Mitigators */}
        <div className="p-3 rounded-lg bg-[#080B10] border border-[#00F5FF]/30">
          <div className="flex items-center gap-1.5 text-xs font-mono font-bold text-[#00F5FF] mb-2">
            <TrendingDown className="w-3.5 h-3.5" />
            Top Benign Anchors (-SHAP)
          </div>
          <ul className="space-y-1 text-[11px] font-mono text-cyber-subtext">
            {top_mitigating_factors && top_mitigating_factors.length > 0 ? (
              top_mitigating_factors.slice(0, 3).map((m, i) => (
                <li key={i} className="flex justify-between">
                  <span className="truncate max-w-[180px]">{m.feature}</span>
                  <span className="text-[#00F5FF] font-bold">{m.shap_value.toFixed(3)}</span>
                </li>
              ))
            ) : (
              <li className="text-cyber-muted">No major mitigating anchors found</li>
            )}
          </ul>
        </div>

      </div>

    </div>
  );
}
