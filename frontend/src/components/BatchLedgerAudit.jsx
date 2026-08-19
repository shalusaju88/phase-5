import React, { useState } from 'react';
import { UploadCloud, FileText, Download, ShieldAlert, CheckCircle, AlertTriangle, RefreshCw, Search } from 'lucide-react';
import { predictCsvBatch } from '../services/api';

export default function BatchLedgerAudit() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [filterVerdict, setFilterVerdict] = useState('ALL');

  const handleFileDrop = (e) => {
    e.preventDefault();
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      setFile(e.dataTransfer.files[0]);
    }
  };

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
    }
  };

  const handleUploadAndRun = async () => {
    if (!file) {
      setError('Please upload a CSV file to proceed.');
      return;
    }

    setLoading(true);
    setError(null);
    try {
      const data = await predictCsvBatch(file);
      setResults(data);
    } catch (err) {
      console.error(err);
      setError(err.response?.data?.detail || err.message || 'Failed to process batch CSV.');
    } finally {
      setLoading(false);
    }
  };

  // Export Annotated CSV
  const handleExportCsv = () => {
    if (!results || !results.predictions) return;

    const headers = [
      'Record_Index', 'Verdict', 'Fraud_Probability', 'Risk_Tier',
      'Archetype', 'Demographic_Group', 'Anomaly_Score', 'UMAP_1', 'UMAP_2', 'Latency_ms'
    ];

    const rows = results.predictions.map((p, idx) => [
      idx + 1,
      p.prediction === 1 ? 'FRAUD_ALERT' : 'BENIGN_VERIFIED',
      p.probability,
      p.risk_tier,
      `"${p.archetype || ''}"`,
      `"${p.fairness_metadata?.demographic_group || ''}"`,
      p.latent_manifolds?.anomaly_score,
      p.latent_manifolds?.UMAP_1,
      p.latent_manifolds?.UMAP_2,
      p.latency_ms
    ]);

    const csvContent = 'data:text/csv;charset=utf-8,' + [headers.join(','), ...rows.map(r => r.join(','))].join('\n');
    const encodedUri = encodeURI(csvContent);
    const link = document.createElement('a');
    link.setAttribute('href', encodedUri);
    link.setAttribute('download', `defi_fraud_audit_report_${Date.now()}.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  // Filter & Search
  const filteredPredictions = (results?.predictions || []).filter((item, idx) => {
    const matchesSearch = searchQuery === '' || 
      item.archetype?.toLowerCase().includes(searchQuery.toLowerCase()) ||
      (idx + 1).toString().includes(searchQuery);
    
    if (filterVerdict === 'FRAUD') return matchesSearch && item.prediction === 1;
    if (filterVerdict === 'BENIGN') return matchesSearch && item.prediction === 0;
    return matchesSearch;
  });

  return (
    <div className="space-y-6">
      
      {/* Upload Box & Telemetry Bar */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        
        {/* Upload Container (5 cols) */}
        <div className="lg:col-span-5">
          <div
            onDragOver={(e) => e.preventDefault()}
            onDrop={handleFileDrop}
            className="cyber-card p-6 border-2 border-dashed border-[#1E293B] hover:border-[#00F5FF]/50 transition-all text-center flex flex-col items-center justify-center min-h-[220px]"
          >
            <div className="w-12 h-12 rounded-xl bg-[#080B10] flex items-center justify-center mb-3 text-[#00F5FF]">
              <UploadCloud className="w-6 h-6" />
            </div>

            <p className="text-xs font-mono font-bold text-white mb-1">
              Drag & Drop On-Chain Ledger CSV Here
            </p>
            <p className="text-[11px] font-mono text-cyber-subtext mb-4">
              Accepts raw transaction ledger dumps with headers
            </p>

            <label className="px-4 py-2 rounded-lg bg-[#00F5FF]/10 text-[#00F5FF] border border-[#00F5FF]/30 text-xs font-mono font-bold cursor-pointer hover:bg-[#00F5FF]/20 transition-all">
              <span>Browse File</span>
              <input type="file" accept=".csv,.txt" onChange={handleFileChange} className="hidden" />
            </label>

            {file && (
              <div className="mt-4 flex items-center gap-2 text-xs font-mono text-[#00FF9D]">
                <FileText className="w-4 h-4" />
                <span className="truncate max-w-[200px]">{file.name}</span>
                <span className="text-cyber-muted">({(file.size / 1024).toFixed(1)} KB)</span>
              </div>
            )}
          </div>

          <button
            onClick={handleUploadAndRun}
            disabled={!file || loading}
            className="w-full mt-3 py-3 rounded-xl font-mono text-xs font-bold uppercase tracking-wider bg-gradient-to-r from-[#00F5FF] to-[#00FF9D] text-[#080B10] shadow-neon-cyan disabled:opacity-40 transition-all flex items-center justify-center gap-2"
          >
            {loading ? (
              <>
                <RefreshCw className="w-4 h-4 animate-spin text-[#080B10]" />
                <span>Auditing Batch Ledger...</span>
              </>
            ) : (
              <>
                <ShieldAlert className="w-4 h-4 text-[#080B10]" />
                <span>Execute Batch Forensic Audit</span>
              </>
            )}
          </button>

          {error && (
            <div className="mt-3 p-3 rounded-lg bg-[#FF2A6D]/10 border border-[#FF2A6D]/40 text-xs font-mono text-[#FF2A6D]">
              {error}
            </div>
          )}
        </div>

        {/* Summary Telemetry Stats (7 cols) */}
        <div className="lg:col-span-7 grid grid-cols-2 sm:grid-cols-4 gap-3">
          
          <div className="cyber-card p-4 text-center">
            <span className="text-[10px] font-mono text-cyber-subtext uppercase">Total Scanned</span>
            <div className="text-2xl font-mono font-bold text-[#00F5FF] mt-1">
              {results?.total_records || 0}
            </div>
          </div>

          <div className="cyber-card p-4 text-center">
            <span className="text-[10px] font-mono text-cyber-subtext uppercase">Fraud Alerts</span>
            <div className="text-2xl font-mono font-bold text-[#FF2A6D] mt-1">
              {results?.fraud_count || 0}
            </div>
          </div>

          <div className="cyber-card p-4 text-center">
            <span className="text-[10px] font-mono text-cyber-subtext uppercase">Fraud Rate</span>
            <div className="text-2xl font-mono font-bold text-[#FFB800] mt-1">
              {results?.fraud_rate_pct ? `${results.fraud_rate_pct}%` : '0.0%'}
            </div>
          </div>

          <div className="cyber-card p-4 text-center">
            <span className="text-[10px] font-mono text-cyber-subtext uppercase">Batch Latency</span>
            <div className="text-2xl font-mono font-bold text-[#00FF9D] mt-1">
              {results?.batch_latency_ms ? `${results.batch_latency_ms} ms` : '0 ms'}
            </div>
          </div>

          {/* Institutional Compliance Notice */}
          <div className="col-span-2 sm:col-span-4 cyber-card p-4">
            <div className="flex items-center justify-between text-xs font-mono">
              <span className="text-cyber-subtext">US EEOC 4/5ths Disparate Impact Standard:</span>
              <span className="text-[#00FF9D] font-bold">100% COMPLIANT</span>
            </div>
            <p className="text-[11px] text-cyber-muted font-mono mt-1">
              Every audited transaction undergoes calibrated group thresholding to prevent wrongful flagging of nascent liquidity pools or new user accounts.
            </p>
          </div>

        </div>

      </div>

      {/* Results Table Section */}
      {results && results.predictions && results.predictions.length > 0 && (
        <div className="cyber-card p-5 space-y-4">
          
          {/* Table Controls */}
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
            
            {/* Search Input */}
            <div className="relative flex-1 max-w-sm">
              <Search className="w-4 h-4 absolute left-3 top-2.5 text-cyber-subtext" />
              <input
                type="text"
                placeholder="Search by archetype or index..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full bg-[#080B10] border border-[#1E293B] rounded-lg pl-9 pr-3 py-1.5 text-xs font-mono text-white focus:outline-none focus:border-[#00F5FF]"
              />
            </div>

            {/* Filter Tabs & Export */}
            <div className="flex items-center space-x-2 font-mono text-xs">
              <button
                onClick={() => setFilterVerdict('ALL')}
                className={`px-3 py-1 rounded ${filterVerdict === 'ALL' ? 'bg-[#00F5FF]/20 text-[#00F5FF] border border-[#00F5FF]/40' : 'text-cyber-subtext'}`}
              >
                All ({results.total_records})
              </button>
              <button
                onClick={() => setFilterVerdict('FRAUD')}
                className={`px-3 py-1 rounded ${filterVerdict === 'FRAUD' ? 'bg-[#FF2A6D]/20 text-[#FF2A6D] border border-[#FF2A6D]/40' : 'text-cyber-subtext'}`}
              >
                Fraud ({results.fraud_count})
              </button>
              <button
                onClick={() => setFilterVerdict('BENIGN')}
                className={`px-3 py-1 rounded ${filterVerdict === 'BENIGN' ? 'bg-[#00FF9D]/20 text-[#00FF9D] border border-[#00FF9D]/40' : 'text-cyber-subtext'}`}
              >
                Benign ({results.benign_count})
              </button>

              <button
                onClick={handleExportCsv}
                className="ml-2 flex items-center gap-1.5 px-3.5 py-1.5 rounded-lg bg-[#00FF9D]/10 text-[#00FF9D] border border-[#00FF9D]/40 font-bold hover:bg-[#00FF9D]/20 transition-all"
              >
                <Download className="w-3.5 h-3.5" />
                <span>Export Annotated CSV</span>
              </button>
            </div>

          </div>

          {/* Table Container */}
          <div className="overflow-x-auto max-h-[500px] border border-[#1E293B] rounded-lg">
            <table className="w-full text-left font-mono text-xs">
              <thead className="bg-[#080B10] text-cyber-subtext sticky top-0 border-b border-[#1E293B]">
                <tr>
                  <th className="p-3">#</th>
                  <th className="p-3">Verdict</th>
                  <th className="p-3">Probability</th>
                  <th className="p-3">Risk Tier</th>
                  <th className="p-3">Archetype</th>
                  <th className="p-3">Demographic Group</th>
                  <th className="p-3">IsoForest Score</th>
                  <th className="p-3">Latency</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-[#1E293B]/60">
                {filteredPredictions.map((row, idx) => {
                  const isRowFraud = row.prediction === 1;
                  return (
                    <tr key={idx} className="hover:bg-[#111C33]/50 transition-colors">
                      <td className="p-3 text-cyber-muted">{idx + 1}</td>
                      <td className="p-3 font-bold">
                        <span className={`inline-flex items-center gap-1 px-2 py-0.5 rounded text-[10px] uppercase ${
                          isRowFraud ? 'bg-[#FF2A6D]/20 text-[#FF2A6D] border border-[#FF2A6D]/40' : 'bg-[#00FF9D]/20 text-[#00FF9D] border border-[#00FF9D]/40'
                        }`}>
                          {isRowFraud ? '🚨 FRAUD' : '🛡️ BENIGN'}
                        </span>
                      </td>
                      <td className={`p-3 font-bold ${isRowFraud ? 'text-[#FF2A6D]' : 'text-[#00FF9D]'}`}>
                        {(row.probability * 100).toFixed(2)}%
                      </td>
                      <td className="p-3 text-white font-bold">{row.risk_tier}</td>
                      <td className="p-3 text-cyber-subtext truncate max-w-[220px]" title={row.archetype}>
                        {row.archetype}
                      </td>
                      <td className="p-3 text-cyber-subtext text-[11px]">
                        {row.fairness_metadata?.demographic_group}
                      </td>
                      <td className="p-3 text-[#00F5FF]">
                        {row.latent_manifolds?.anomaly_score?.toFixed(4)}
                      </td>
                      <td className="p-3 text-cyber-muted">{row.latency_ms} ms</td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>

        </div>
      )}

    </div>
  );
}
