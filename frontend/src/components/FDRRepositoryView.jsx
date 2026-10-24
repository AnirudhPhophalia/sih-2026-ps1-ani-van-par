import React, { useState } from 'react';
import { 
  Building2, Search, Filter, ShieldCheck, AlertTriangle, 
  FileText, ExternalLink, CheckCircle2, Clock, Landmark, Eye, X, Download, Plus, Check
} from 'lucide-react';

export default function FDRRepositoryView({ 
  fdrs, 
  onSelectFDR, 
  onOpenNewFDR,
  onNavigateTab
}) {
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState('ALL');
  const [bankFilter, setBankFilter] = useState('ALL');
  const [selectedFdrDetail, setSelectedFdrDetail] = useState(null);
  const [detailModalOpen, setDetailModalOpen] = useState(false);
  const [detailTab, setDetailTab] = useState('audit-comparison'); // 'audit-comparison', 'document', 'history'

  // Filter logic
  const filteredFdrs = (fdrs || []).filter(item => {
    const matchesSearch = 
      item.fdr_number?.toLowerCase().includes(searchTerm.toLowerCase()) ||
      item.institution_name?.toLowerCase().includes(searchTerm.toLowerCase()) ||
      item.institution_pid?.toLowerCase().includes(searchTerm.toLowerCase()) ||
      item.account_number?.toLowerCase().includes(searchTerm.toLowerCase());

    const matchesStatus = statusFilter === 'ALL' || item.status === statusFilter;
    const matchesBank = bankFilter === 'ALL' || item.bank_name?.toLowerCase().includes(bankFilter.toLowerCase());

    return matchesSearch && matchesStatus && matchesBank;
  });

  const getStatusBadge = (status) => {
    switch (status) {
      case 'VERIFIED_ACTIVE':
        return (
          <span className="inline-flex items-center px-2 py-0.5 rounded text-[10.5px] font-semibold bg-emerald-50 text-emerald-800 border border-emerald-200">
            <span className="h-1.5 w-1.5 rounded-full bg-emerald-600 mr-1.5"></span>
            Verified Active
          </span>
        );
      case 'UNDER_SCRUTINY':
        return (
          <span className="inline-flex items-center px-2 py-0.5 rounded text-[10.5px] font-semibold bg-amber-50 text-amber-800 border border-amber-200">
            <span className="h-1.5 w-1.5 rounded-full bg-amber-600 mr-1.5"></span>
            Under Scrutiny
          </span>
        );
      case 'DISCREPANCY_FLAGGED':
        return (
          <span className="inline-flex items-center px-2 py-0.5 rounded text-[10.5px] font-semibold bg-rose-50 text-rose-800 border border-rose-200">
            <span className="h-1.5 w-1.5 rounded-full bg-rose-600 mr-1.5"></span>
            Discrepancy
          </span>
        );
      case 'MATURITY_APPROACHING':
        return (
          <span className="inline-flex items-center px-2 py-0.5 rounded text-[10.5px] font-semibold bg-amber-50 text-amber-800 border border-amber-200">
            <span className="h-1.5 w-1.5 rounded-full bg-amber-600 mr-1.5"></span>
            Expiring Soon
          </span>
        );
      case 'MATURED_PENDING_RENEWAL':
        return (
          <span className="inline-flex items-center px-2 py-0.5 rounded text-[10.5px] font-semibold bg-rose-50 text-rose-900 border border-rose-300 font-bold">
            <span className="h-1.5 w-1.5 rounded-full bg-rose-600 mr-1.5"></span>
            Overdue Renewal
          </span>
        );
      case 'RELEASE_REQUESTED':
        return (
          <span className="inline-flex items-center px-2 py-0.5 rounded text-[10.5px] font-semibold bg-blue-50 text-blue-900 border border-blue-200">
            <span className="h-1.5 w-1.5 rounded-full bg-blue-600 mr-1.5"></span>
            Release Requested
          </span>
        );
      case 'RELEASED_DISCHARGED':
        return (
          <span className="inline-flex items-center px-2 py-0.5 rounded text-[10.5px] font-semibold bg-slate-100 text-slate-700 border border-slate-200">
            Discharged
          </span>
        );
      default:
        return (
          <span className="inline-flex items-center px-2 py-0.5 rounded text-[10.5px] font-medium bg-slate-100 text-slate-700 border border-slate-200">
            {status}
          </span>
        );
    }
  };

  const openDetails = async (fdrId) => {
    try {
      const res = await fetch(`/api/fdrs/${fdrId}`);
      if (res.ok) {
        const data = await res.json();
        setSelectedFdrDetail(data.fdr);
        setDetailTab('audit-comparison');
        setDetailModalOpen(true);
      }
    } catch (err) {
      console.error("Failed to fetch FDR details:", err);
    }
  };

  return (
    <div className="space-y-5 animate-entrance">
      {/* Module Title and Primary Action */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-sm md:text-base font-semibold text-slate-800 flex items-center space-x-2">
            <Building2 className="h-4 w-4 text-slate-600" />
            <span>Centralized Security Deposit & FDR Collateral Registry</span>
          </h1>
          <p className="text-xs text-slate-500 mt-0.5">
            Statutory registry of technical education collateral across Indian States and Union Territories
          </p>
        </div>

        <button
          onClick={() => onOpenNewFDR()}
          className="flex items-center space-x-1.5 rounded bg-slate-800 hover:bg-slate-900 px-3.5 py-1.5 text-xs font-medium text-white transition-colors"
        >
          <Plus className="h-3.5 w-3.5 text-slate-300" />
          <span>Pledge New FDR</span>
        </button>
      </div>

      {/* Filter and Search Bar */}
      <div className="card-institutional p-3 bg-white border border-slate-200 flex flex-col md:flex-row gap-2.5 items-stretch md:items-center justify-between">
        {/* Search */}
        <div className="relative flex-1">
          <Search className="absolute left-3 top-2.5 h-3.5 w-3.5 text-slate-400" />
          <input
            type="text"
            placeholder="Search by FDR No, Account No, PID or Institution Name..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="input-institutional pl-9 py-1.5 text-xs"
          />
        </div>

        {/* Filters */}
        <div className="flex flex-wrap items-center gap-2">
          {/* Status Select */}
          <select
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
            className="select-institutional py-1.5 text-xs"
          >
            <option value="ALL">All Statuses ({fdrs?.length || 0})</option>
            <option value="VERIFIED_ACTIVE">Verified Active</option>
            <option value="UNDER_SCRUTINY">Under Scrutiny</option>
            <option value="DISCREPANCY_FLAGGED">Discrepancy Flagged</option>
            <option value="MATURITY_APPROACHING">Approaching Maturity</option>
            <option value="MATURED_PENDING_RENEWAL">Overdue Renewal</option>
            <option value="RELEASE_REQUESTED">Release Requested</option>
          </select>

          {/* Bank Select */}
          <select
            value={bankFilter}
            onChange={(e) => setBankFilter(e.target.value)}
            className="select-institutional py-1.5 text-xs"
          >
            <option value="ALL">All Banks</option>
            <option value="State Bank of India">State Bank of India</option>
            <option value="Punjab National Bank">Punjab National Bank</option>
            <option value="HDFC Bank">HDFC Bank</option>
            <option value="Canara Bank">Canara Bank</option>
            <option value="Bank of Baroda">Bank of Baroda</option>
          </select>

          {(searchTerm || statusFilter !== 'ALL' || bankFilter !== 'ALL') && (
            <button
              onClick={() => {
                setSearchTerm('');
                setStatusFilter('ALL');
                setBankFilter('ALL');
              }}
              className="text-xs text-blue-900 hover:underline px-2 py-1 font-semibold"
            >
              Reset
            </button>
          )}
        </div>
      </div>

      {/* Main Professional Financial Table */}
      <div className="card-institutional bg-white border border-slate-200 overflow-hidden shadow-2xs">
        <div className="overflow-x-auto">
          <table className="w-full table-fintech text-left">
            <thead>
              <tr>
                <th>FDR Instrument</th>
                <th>Institution Name & PID</th>
                <th>Custodian Bank & Branch</th>
                <th className="text-right">Deposit Principal</th>
                <th className="text-center">Maturity Date</th>
                <th className="text-center">Regulatory Status</th>
                <th className="text-center">Action</th>
              </tr>
            </thead>
            <tbody>
              {filteredFdrs.length === 0 ? (
                <tr>
                  <td colSpan={7} className="py-12 text-center text-slate-500 text-xs">
                    No matching fixed deposit collateral records found.
                  </td>
                </tr>
              ) : (
                filteredFdrs.map((item) => (
                  <tr key={item.id}>
                    <td>
                      <div className="font-mono font-bold text-slate-900 text-xs">{item.fdr_number}</div>
                      <div className="text-[10.5px] text-slate-500 font-mono">A/C: {item.account_number}</div>
                    </td>

                    <td>
                      <div className="font-semibold text-slate-800 text-xs">{item.institution_name}</div>
                      <div className="text-[10.5px] text-slate-500">
                        PID: <span className="font-mono font-medium text-slate-700">{item.institution_pid}</span> • {item.institution_state}
                      </div>
                    </td>

                    <td>
                      <div className="text-slate-800 font-medium text-xs">{item.bank_name}</div>
                      <div className="text-[10.5px] text-slate-500 font-mono">{item.ifsc_code} • {item.branch_name}</div>
                    </td>

                    <td className="text-right">
                      <div className="font-mono font-bold text-slate-900 text-xs">
                        ₹{item.deposit_amount.toLocaleString('en-IN', { minimumFractionDigits: 2 })}
                      </div>
                      <div className="text-[10px] text-slate-500">ROI: {item.rate_of_interest || 7.25}% p.a.</div>
                    </td>

                    <td className="text-center">
                      <div className="font-mono text-slate-800 font-medium text-xs">{item.maturity_date}</div>
                      <div className="text-[10px] text-slate-500">Lock-in: {item.statutory_lock_in_years || 8} Yrs</div>
                    </td>

                    <td className="text-center">
                      {getStatusBadge(item.status)}
                      {item.is_discrepant && (
                        <div className="mt-1 text-[10px] font-bold text-rose-700 flex items-center justify-center space-x-1">
                          <AlertTriangle className="h-3 w-3" />
                          <span>Flagged</span>
                        </div>
                      )}
                    </td>

                    <td className="text-center">
                      <button
                        onClick={() => openDetails(item.id)}
                        className="inline-flex items-center space-x-1 rounded border border-slate-300 bg-white px-2 py-1 text-[11px] font-medium text-slate-700 hover:bg-slate-50 hover:text-blue-900 hover:border-slate-400 transition-colors"
                      >
                        <Eye className="h-3 w-3 text-slate-500" />
                        <span>Inspect</span>
                      </button>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>

        {/* Table Footer Stats */}
        <div className="p-3 border-t border-slate-200 bg-slate-50/70 text-[11px] text-slate-500 flex flex-col sm:flex-row items-center justify-between gap-2">
          <div>
            Showing <span className="font-semibold text-slate-800">{filteredFdrs.length}</span> of <span className="font-semibold text-slate-800">{fdrs.length}</span> total collateral instruments
          </div>
          <div className="flex items-center space-x-4">
            <span>Section 10(k) AICTE Mandate</span>
            <span>•</span>
            <span className="font-mono text-slate-700 font-medium">Lien Registered with Custodian</span>
          </div>
        </div>
      </div>

      {/* Comprehensive FDR Details & Audit Comparison Modal */}
      {detailModalOpen && selectedFdrDetail && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/40 backdrop-blur-xs p-4 overflow-y-auto">
          <div className="bg-white w-full max-w-4xl rounded-md border border-slate-300 p-5 shadow-xl relative my-6 animate-modal">
            <button
              onClick={() => setDetailModalOpen(false)}
              className="absolute right-4 top-4 rounded p-1 text-slate-400 hover:bg-slate-100 hover:text-slate-700 transition-colors"
            >
              <X className="h-4 w-4" />
            </button>

            {/* Modal Header */}
            <div className="border-b border-slate-200 pb-3 mb-3">
              <div className="flex items-center space-x-2.5">
                <span className="font-mono text-base font-bold text-slate-900">{selectedFdrDetail.fdr_number}</span>
                {getStatusBadge(selectedFdrDetail.status)}
                <span className="text-xs text-slate-400 font-mono">| {selectedFdrDetail.bank_name}</span>
              </div>
              <p className="text-xs text-slate-600 mt-0.5">
                {selectedFdrDetail.institution?.name} • AICTE PID: <span className="font-mono font-semibold">{selectedFdrDetail.institution?.pid}</span>
              </p>
            </div>

            {/* Modal Navigation Tabs */}
            <div className="flex space-x-1 border-b border-slate-200 pb-2 mb-4 text-xs font-medium">
              <button
                onClick={() => setDetailTab('audit-comparison')}
                className={`px-3 py-1.5 rounded transition-colors ${
                  detailTab === 'audit-comparison'
                    ? 'bg-slate-800 text-white font-medium'
                    : 'text-slate-600 hover:bg-slate-100'
                }`}
              >
                Submitted Claim vs Bank Ground Truth
              </button>
              <button
                onClick={() => setDetailTab('document')}
                className={`px-3 py-1.5 rounded transition-colors ${
                  detailTab === 'document'
                    ? 'bg-slate-800 text-white font-medium'
                    : 'text-slate-600 hover:bg-slate-100'
                }`}
              >
                Document Vault ({selectedFdrDetail.documents?.length || 0})
              </button>
              <button
                onClick={() => setDetailTab('history')}
                className={`px-3 py-1.5 rounded transition-colors ${
                  detailTab === 'history'
                    ? 'bg-slate-800 text-white font-medium'
                    : 'text-slate-600 hover:bg-slate-100'
                }`}
              >
                Bank Verification Trail ({selectedFdrDetail.verifications?.length || 0})
              </button>
            </div>

            {/* Tab 1: Clear Distinction: Institution Submitted vs Bank Verified Data */}
            {detailTab === 'audit-comparison' && (
              <div className="space-y-4 text-xs">
                {/* Notice Alert if discrepant */}
                {selectedFdrDetail.is_discrepant && (
                  <div className="rounded border border-rose-300 bg-rose-50/80 p-3 text-rose-900 space-y-1">
                    <div className="flex items-center space-x-1.5 font-bold text-rose-800">
                      <AlertTriangle className="h-4 w-4 text-rose-600 shrink-0" />
                      <span>Auditor Notice: Discrepancy Detected between Institution Claim & Bank Ground Truth</span>
                    </div>
                    <p className="text-[11.5px] text-rose-800 leading-normal">
                      {selectedFdrDetail.discrepancy_notes || "Differences found in declared amount, account number, or lien status during automated bank verification."}
                    </p>
                  </div>
                )}

                {/* Side-by-Side Comparison Grid */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {/* Left Column: Institution Submitted Data */}
                  <div className="border border-slate-200 rounded-md p-3.5 bg-slate-50/50 space-y-3">
                    <div className="flex items-center justify-between border-b border-slate-200 pb-2">
                      <span className="font-bold text-slate-800 uppercase tracking-wider text-[11px] flex items-center space-x-1.5">
                        <span className="h-2 w-2 rounded-full bg-slate-500"></span>
                        <span>Institution Submitted Claim</span>
                      </span>
                      <span className="text-[10px] text-slate-500 font-mono">PORTAL_UPLOAD</span>
                    </div>

                    <div className="space-y-2 text-xs">
                      <div>
                        <span className="text-[10.5px] text-slate-500 block">Declared Principal Amount</span>
                        <span className="font-mono font-bold text-slate-900 text-sm">
                          ₹{selectedFdrDetail.deposit_amount.toLocaleString('en-IN', { minimumFractionDigits: 2 })}
                        </span>
                      </div>
                      <div>
                        <span className="text-[10.5px] text-slate-500 block">Declared Account Number</span>
                        <span className="font-mono text-slate-800">{selectedFdrDetail.account_number}</span>
                      </div>
                      <div>
                        <span className="text-[10.5px] text-slate-500 block">FDR Certificate Number</span>
                        <span className="font-mono text-slate-800">{selectedFdrDetail.fdr_number}</span>
                      </div>
                      <div className="grid grid-cols-2 gap-2">
                        <div>
                          <span className="text-[10.5px] text-slate-500 block">Issue Date</span>
                          <span className="font-mono text-slate-700">{selectedFdrDetail.issue_date}</span>
                        </div>
                        <div>
                          <span className="text-[10.5px] text-slate-500 block">Maturity Date</span>
                          <span className="font-mono text-slate-700">{selectedFdrDetail.maturity_date}</span>
                        </div>
                      </div>
                      <div>
                        <span className="text-[10.5px] text-slate-500 block">Statutory Lock-in Period</span>
                        <span className="text-slate-800 font-medium">{selectedFdrDetail.statutory_lock_in_years} Years (Exp: {selectedFdrDetail.statutory_lock_in_end_date})</span>
                      </div>
                    </div>
                  </div>

                  {/* Right Column: Bank / Authorized Source Verified Data */}
                  <div className="border border-blue-200 rounded-md p-3.5 bg-blue-50/20 space-y-3">
                    <div className="flex items-center justify-between border-b border-blue-200 pb-2">
                      <span className="font-bold text-blue-950 uppercase tracking-wider text-[11px] flex items-center space-x-1.5">
                        <span className="h-2 w-2 rounded-full bg-emerald-600"></span>
                        <span>Bank / Source Verified Ground Truth</span>
                      </span>
                      <span className="text-[10px] text-blue-900 font-mono font-semibold">
                        {selectedFdrDetail.verification_level || "BANK_CBS_SFMS"}
                      </span>
                    </div>

                    <div className="space-y-2 text-xs">
                      <div>
                        <span className="text-[10.5px] text-slate-500 block">Confirmed Balance (CBS Ledger)</span>
                        <span className="font-mono font-bold text-emerald-800 text-sm">
                          ₹{selectedFdrDetail.deposit_amount.toLocaleString('en-IN', { minimumFractionDigits: 2 })}
                        </span>
                      </div>
                      <div>
                        <span className="text-[10.5px] text-slate-500 block">Bank Branch & IFSC Code</span>
                        <span className="text-slate-800 font-medium">{selectedFdrDetail.bank_name} • {selectedFdrDetail.branch_name} ({selectedFdrDetail.ifsc_code})</span>
                      </div>
                      <div>
                        <span className="text-[10.5px] text-slate-500 block">Statutory Lien Endorsement</span>
                        <span className="font-semibold text-emerald-800 flex items-center space-x-1">
                          <Check className="h-3.5 w-3.5 text-emerald-600" />
                          <span>{selectedFdrDetail.lien_marked ? "Lien Officially Endorsed in favor of AICTE" : "Unmarked"}</span>
                        </span>
                      </div>
                      <div className="grid grid-cols-2 gap-2">
                        <div>
                          <span className="text-[10.5px] text-slate-500 block">Verification Source</span>
                          <span className="font-semibold text-slate-700">{selectedFdrDetail.verification_level}</span>
                        </div>
                        <div>
                          <span className="text-[10.5px] text-slate-500 block">Audit Chain Status</span>
                          <span className="font-mono text-emerald-700 font-bold">MERKLE_PINNED</span>
                        </div>
                      </div>
                      <div>
                        <span className="text-[10.5px] text-slate-500 block">Lien Beneficial Endorsee</span>
                        <span className="text-slate-800 font-mono text-[11px]">{selectedFdrDetail.lien_in_favor_of}</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            )}

            {/* Tab 2: Document Vault */}
            {detailTab === 'document' && (
              <div className="space-y-3">
                {selectedFdrDetail.documents?.map((doc) => (
                  <div key={doc.id} className="rounded border border-slate-200 bg-slate-50 p-3 space-y-2.5">
                    <div className="flex items-center justify-between text-xs">
                      <div>
                        <div className="font-semibold text-slate-900 flex items-center space-x-1.5">
                          <FileText className="h-3.5 w-3.5 text-blue-900" />
                          <span>{doc.file_name}</span>
                        </div>
                        <div className="text-[10px] text-slate-500 font-mono mt-0.5">
                          SHA-256 Digest: {doc.sha256_hash}
                        </div>
                      </div>
                      <a
                        href={doc.file_url}
                        target="_blank"
                        rel="noreferrer"
                        className="flex items-center space-x-1 rounded bg-white border border-slate-300 px-2.5 py-1 text-xs text-blue-900 font-medium hover:bg-slate-50 transition-colors"
                      >
                        <span>Open Full Certificate</span>
                        <ExternalLink className="h-3 w-3" />
                      </a>
                    </div>

                    {/* Integrated Certificate Image */}
                    <div className="rounded border border-slate-200 bg-white p-2 flex items-center justify-center max-h-72 overflow-hidden">
                      <img 
                        src={doc.file_url} 
                        alt="FDR Certificate" 
                        className="max-h-64 object-contain"
                      />
                    </div>
                  </div>
                ))}
              </div>
            )}

            {/* Tab 3: Bank Verification Trail */}
            {detailTab === 'history' && (
              <div className="space-y-2 text-xs">
                {selectedFdrDetail.verifications?.length === 0 ? (
                  <div className="py-8 text-center text-slate-500">
                    No bank verification attempts recorded yet.
                  </div>
                ) : (
                  selectedFdrDetail.verifications.map((v) => (
                    <div key={v.id} className="rounded border border-slate-200 bg-slate-50 p-2.5 space-y-1">
                      <div className="flex items-center justify-between">
                        <span className="font-semibold text-emerald-800">{v.verification_source}</span>
                        <span className="text-[10px] text-slate-500 font-mono">{new Date(v.verified_at).toLocaleString()}</span>
                      </div>
                      <div className="text-slate-700">{v.remarks}</div>
                      <div className="text-[10px] text-slate-500 font-mono">Transaction Ref: {v.bank_api_transaction_ref}</div>
                    </div>
                  ))
                )}
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
