import React, { useState, useEffect } from 'react';
import { 
  ShieldCheck, AlertTriangle, CheckCircle2, RefreshCw, 
  FileText, ArrowRight, Check, X, ShieldAlert, Cpu, Sparkles
} from 'lucide-react';

export default function ScrutinyDeskView({ onRefreshAll }) {
  const [queue, setQueue] = useState([]);
  const [selectedFdr, setSelectedFdr] = useState(null);
  const [loading, setLoading] = useState(false);
  const [scanning, setScanning] = useState(false);
  const [scanResult, setScanResult] = useState(null);
  const [officerRemarks, setOfficerRemarks] = useState('');
  const [actionSuccessMsg, setActionSuccessMsg] = useState(null);

  const fetchQueue = async () => {
    setLoading(true);
    try {
      const res = await fetch('/api/scrutiny/queue');
      if (res.ok) {
        const data = await res.json();
        setQueue(data.queue || []);
        if (data.queue?.length > 0 && !selectedFdr) {
          selectQueueItem(data.queue[0]);
        }
      }
    } catch (err) {
      console.error("Failed to load scrutiny queue:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchQueue();
  }, []);

  const selectQueueItem = async (item) => {
    setSelectedFdr(item);
    setScanResult(null);
    setActionSuccessMsg(null);
    setOfficerRemarks('');

    try {
      const res = await fetch(`/api/fdrs/${item.id}`);
      if (res.ok) {
        const data = await res.json();
        setSelectedFdr(prev => ({ ...prev, ...data.fdr }));
      }
    } catch (err) {
      console.error("Failed to fetch FDR details:", err);
    }
  };

  const handleRunAiScan = async () => {
    if (!selectedFdr) return;
    setScanning(true);
    setActionSuccessMsg(null);
    try {
      const res = await fetch(`/api/scrutiny/scan/${selectedFdr.id}`, {
        method: 'POST'
      });
      if (res.ok) {
        const data = await res.json();
        setScanResult(data);
      }
    } catch (err) {
      console.error("Failed to run OCR scan:", err);
    } finally {
      setScanning(false);
    }
  };

  const handleOfficerDecision = async (action) => {
    if (!selectedFdr) return;
    try {
      const res = await fetch(`/api/scrutiny/action/${selectedFdr.id}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          action: action,
          officer_id: "AICTE_SCRUTINY_OFFICER_01",
          remarks: officerRemarks || (action === 'APPROVE' ? "Compliant with APH guidelines." : "Discrepancy flagged.")
        })
      });
      if (res.ok) {
        setActionSuccessMsg(`Regulatory order '${action}' recorded in Merkle audit ledger.`);
        fetchQueue();
        onRefreshAll?.();
      }
    } catch (err) {
      console.error("Failed to submit scrutiny decision:", err);
    }
  };

  return (
    <div className="space-y-5 animate-entrance">
      {/* Title */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-sm md:text-base font-semibold text-slate-800 flex items-center space-x-2">
            <ShieldCheck className="h-4 w-4 text-slate-600" />
            <span>AI Document Forensics & Scrutiny Desk</span>
          </h1>
          <p className="text-xs text-slate-500 mt-0.5">
            Automated OCR extraction, Error Level Analysis (ELA) tampering detection, and mathematical discrepancy scoring
          </p>
        </div>

        <button
          onClick={fetchQueue}
          disabled={loading}
          className="flex items-center space-x-1.5 rounded-md bg-white border border-slate-300 hover:bg-slate-50 px-3 py-1.5 text-xs text-slate-700 font-medium transition-colors disabled:opacity-50"
        >
          <RefreshCw className={`h-3.5 w-3.5 text-slate-500 ${loading ? 'animate-spin' : ''}`} />
          <span>Refresh Queue ({queue.length})</span>
        </button>
      </div>

      {actionSuccessMsg && (
        <div className="rounded-md border border-emerald-300 bg-emerald-50 p-3 text-xs font-semibold text-emerald-900 flex items-center space-x-2 shadow-2xs">
          <CheckCircle2 className="h-4 w-4 text-emerald-600 shrink-0" />
          <span>{actionSuccessMsg}</span>
        </div>
      )}

      {/* Main Two-Column Layout */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-5">
        {/* Left Col: Pending Scrutiny Queue (4 Cols) */}
        <div className="lg:col-span-4 card-institutional p-4 bg-white border border-slate-200 space-y-3">
          <div className="flex items-center justify-between text-xs font-bold text-slate-800 border-b border-slate-200 pb-2">
            <span>Pending Inspection Queue</span>
            <span className="rounded bg-slate-100 text-slate-700 px-2 py-0.5 text-[10.5px] font-mono border border-slate-200">
              {queue.length} Pending
            </span>
          </div>

          <div className="space-y-2 max-h-[580px] overflow-y-auto pr-1">
            {queue.length === 0 ? (
              <div className="py-12 text-center text-xs text-slate-500">
                Queue is clear. No instruments pending regulatory scrutiny.
              </div>
            ) : (
              queue.map((item) => {
                const isSelected = selectedFdr?.id === item.id;
                return (
                  <div
                    key={item.id}
                    onClick={() => selectQueueItem(item)}
                    className={`p-3 rounded-md border text-xs cursor-pointer transition-colors ${
                      isSelected
                        ? 'bg-blue-50/80 border-blue-900 text-slate-900 shadow-2xs'
                        : 'bg-white border-slate-200 text-slate-700 hover:border-slate-300 hover:bg-slate-50'
                    }`}
                  >
                    <div className="flex items-center justify-between">
                      <span className="font-mono font-bold text-slate-900">{item.fdr_number}</span>
                      <span className="text-[10.5px] text-slate-600 font-mono font-semibold">
                        ₹{(item.deposit_amount / 100000).toFixed(1)}L
                      </span>
                    </div>

                    <div className="font-medium text-slate-800 truncate mt-1">{item.institution_name}</div>
                    <div className="text-[10.5px] text-slate-500 flex items-center justify-between mt-1">
                      <span>{item.bank_name}</span>
                      <span className={`px-1.5 py-0.2 rounded text-[9.5px] font-semibold ${
                        item.status === 'DISCREPANCY_FLAGGED'
                          ? 'bg-rose-50 text-rose-800 border border-rose-200'
                          : 'bg-amber-50 text-amber-800 border border-amber-200'
                      }`}>
                        {item.status === 'DISCREPANCY_FLAGGED' ? 'DISCREPANT' : 'PENDING'}
                      </span>
                    </div>
                  </div>
                );
              })
            )}
          </div>
        </div>

        {/* Right Col: Side-by-Side Scrutiny Workspace (8 Cols) */}
        <div className="lg:col-span-8 space-y-4">
          {!selectedFdr ? (
            <div className="card-institutional p-12 text-center text-slate-500 border border-slate-200 text-xs">
              Select an instrument from the scrutiny queue to begin inspection.
            </div>
          ) : (
            <div className="space-y-4">
              {/* Header Info Bar */}
              <div className="card-institutional p-3.5 bg-white border border-slate-200 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
                <div>
                  <div className="flex items-center space-x-2">
                    <span className="font-mono text-sm font-bold text-slate-900">{selectedFdr.fdr_number}</span>
                    <span className="text-xs text-slate-500 font-medium">({selectedFdr.bank_name})</span>
                  </div>
                  <p className="text-xs text-slate-600 mt-0.5">
                    {selectedFdr.institution_name || selectedFdr.institution?.name} • PID: <span className="font-mono font-medium">{selectedFdr.institution_pid || selectedFdr.institution?.pid}</span>
                  </p>
                </div>

                <button
                  onClick={handleRunAiScan}
                  disabled={scanning}
                  className="flex items-center space-x-1.5 rounded bg-slate-800 hover:bg-slate-900 px-3.5 py-1.5 text-xs font-medium text-white disabled:opacity-50 transition-colors"
                >
                  <Cpu className={`h-3.5 w-3.5 text-slate-300 ${scanning ? 'animate-spin' : ''}`} />
                  <span>{scanning ? 'Running Forensics...' : 'Execute AI Forensic Scan'}</span>
                </button>
              </div>

              {/* Side-by-Side View */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {/* Left Pane: Uploaded Certificate Preview */}
                <div className="card-institutional p-3.5 bg-white border border-slate-200 space-y-2.5">
                  <div className="flex items-center justify-between text-xs font-bold text-slate-800 border-b border-slate-200 pb-2">
                    <span className="flex items-center space-x-1.5">
                      <FileText className="h-3.5 w-3.5 text-blue-900" />
                      <span>Submitted Bank Certificate</span>
                    </span>
                    <span className="text-[10px] text-slate-500 font-mono">DIGITAL_VAULT</span>
                  </div>

                  <div className="rounded border border-slate-200 bg-slate-50 p-2 flex items-center justify-center min-h-[260px]">
                    {selectedFdr.documents?.[0]?.file_url ? (
                      <img 
                        src={selectedFdr.documents[0].file_url} 
                        alt="FDR Certificate Scan" 
                        className="max-h-60 object-contain"
                      />
                    ) : (
                      <div className="text-slate-400 text-xs">No scan preview available</div>
                    )}
                  </div>

                  <div className="text-[10px] text-slate-500 font-mono break-all bg-slate-50 p-2 rounded border border-slate-200">
                    <span className="text-slate-700 font-semibold">SHA-256 Digest: </span>
                    {selectedFdr.documents?.[0]?.sha256_hash || "Computing hash..."}
                  </div>
                </div>

                {/* Right Pane: AI OCR Extraction & Discrepancy Gauge */}
                <div className="card-institutional p-3.5 bg-white border border-slate-200 space-y-2.5">
                  <div className="flex items-center justify-between text-xs font-bold text-slate-800 border-b border-slate-200 pb-2">
                    <span className="flex items-center space-x-1.5">
                      <Cpu className="h-3.5 w-3.5 text-blue-900" />
                      <span>OCR Extraction & Discrepancy Diff</span>
                    </span>
                    {scanResult && (
                      <span className={`px-2 py-0.2 rounded text-[10px] font-semibold ${
                        scanResult.is_discrepant ? 'bg-rose-50 text-rose-800 border border-rose-200' : 'bg-emerald-50 text-emerald-800 border border-emerald-200'
                      }`}>
                        {scanResult.is_discrepant ? 'DELTA DETECTED' : '100% MATCH'}
                      </span>
                    )}
                  </div>

                  {!scanResult ? (
                    <div className="py-16 text-center text-xs text-slate-500 space-y-2">
                      <Cpu className="h-6 w-6 text-slate-400 mx-auto" />
                      <p className="max-w-xs mx-auto text-slate-500">
                        Click "Execute AI Forensic Scan" above to extract tabular certificate text and compute Levenshtein discrepancy metrics.
                      </p>
                    </div>
                  ) : (
                    <div className="space-y-3 text-xs">
                      {/* Discrepancy Score Meter */}
                      <div className="p-2.5 rounded bg-slate-50 border border-slate-200">
                        <div className="flex items-center justify-between">
                          <span className="text-[11px] font-semibold text-slate-600">Discrepancy Metric (Δ_score)</span>
                          <span className={`font-mono font-bold ${scanResult.discrepancy_score > 0.05 ? 'text-rose-700' : 'text-emerald-700'}`}>
                            {scanResult.discrepancy_score.toFixed(4)} (Threshold: 0.0500)
                          </span>
                        </div>
                        <div className="mt-1.5 h-1.5 w-full bg-slate-200 rounded-full overflow-hidden">
                          <div 
                            className={`h-full rounded-full transition-all duration-300 ${scanResult.discrepancy_score > 0.05 ? 'bg-rose-600' : 'bg-emerald-600'}`}
                            style={{ width: `${Math.min(100, Math.max(5, scanResult.discrepancy_score * 500))}%` }}
                          ></div>
                        </div>
                      </div>

                      {/* Field Comparisons Table */}
                      <div className="space-y-1">
                        {Object.entries(scanResult.field_comparisons || {}).map(([key, item]) => (
                          <div 
                            key={key} 
                            className={`p-2 rounded border text-[11px] flex items-center justify-between ${
                              item.match 
                                ? 'bg-slate-50/80 border-slate-200 text-slate-700' 
                                : 'bg-rose-50/70 border-rose-300 text-rose-900'
                            }`}
                          >
                            <div>
                              <span className="font-semibold capitalize text-slate-800">{key.replace('_', ' ')}:</span>
                              <div className="text-[10px] text-slate-500">
                                Declared: <span className="font-mono text-slate-700">{String(item.declared)}</span>
                              </div>
                            </div>

                            <div className="text-right">
                              <span className="text-[10px] text-slate-500">OCR Extracted:</span>
                              <div className={`font-mono font-semibold ${item.match ? 'text-emerald-700' : 'text-rose-700'}`}>
                                {String(item.ocr)}
                              </div>
                            </div>
                          </div>
                        ))}
                      </div>

                      {/* ELA Forensic Tag */}
                      <div className="flex items-center justify-between text-[10.5px] text-slate-600 bg-slate-50 p-2 rounded border border-slate-200">
                        <span className="font-medium">Error Level Analysis (ELA):</span>
                        <span className="font-mono font-bold text-emerald-800">
                          {scanResult.forensics?.forensic_status || "CLEAN_GENUINE"} (P: {scanResult.forensics?.tamper_probability || 0.02})
                        </span>
                      </div>
                    </div>
                  )}
                </div>
              </div>

              {/* Official Decision Action Box */}
              <div className="card-institutional p-3.5 bg-white border border-slate-200 space-y-2.5">
                <div className="text-xs font-bold text-slate-800">
                  Regulatory Scrutiny Order & Decision Entry
                </div>

                <input
                  type="text"
                  placeholder="Official compliance review notes..."
                  value={officerRemarks}
                  onChange={(e) => setOfficerRemarks(e.target.value)}
                  className="input-institutional text-xs py-1.5"
                />

                <div className="flex flex-wrap items-center justify-end gap-2 pt-1">
                  <button
                    onClick={() => handleOfficerDecision('FLAG_DISCREPANCY')}
                    className="flex items-center space-x-1 rounded border border-rose-300 bg-rose-50 px-3 py-1.5 text-xs font-semibold text-rose-800 hover:bg-rose-100 transition-colors"
                  >
                    <X className="h-3.5 w-3.5" />
                    <span>Flag Discrepancy & Issue Notice</span>
                  </button>

                  <button
                    onClick={() => handleOfficerDecision('FORWARD_TO_BANK')}
                    className="flex items-center space-x-1 rounded border border-slate-300 bg-white px-3 py-1.5 text-xs font-semibold text-slate-700 hover:bg-slate-50 transition-colors"
                  >
                    <ShieldAlert className="h-3.5 w-3.5 text-slate-500" />
                    <span>Send for Bank Telemetry</span>
                  </button>

                  <button
                    onClick={() => handleOfficerDecision('APPROVE')}
                    className="flex items-center space-x-1 rounded bg-emerald-700 hover:bg-emerald-800 px-4 py-1.5 text-xs font-semibold text-white shadow-xs transition-colors"
                  >
                    <Check className="h-3.5 w-3.5" />
                    <span>Approve & Verify Instrument</span>
                  </button>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
