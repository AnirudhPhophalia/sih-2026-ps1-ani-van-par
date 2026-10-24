import sys
import subprocess
import uvicorn
from pathlib import Path

def main():
    print("=" * 75)
    print("  AICTE SECURITY DEPOSIT & FIXED DEPOSIT RECEIPT (FDR) MANAGEMENT PORTAL")
    print("  Ministry of Education, Government of India • Regulation Bureau")
    print("=" * 75)
    print("\n[+] Starting Zero-Trust FastAPI & Frontend Server...")
    print("    • Backend REST API & OpenAPI Docs : http://127.0.0.1:8000/docs")
    print("    • Full Interactive Web Portal      : http://127.0.0.1:8000")
    print("    • Merkle Ledger Integrity Check   : http://127.0.0.1:8000/api/audit/verify-chain")
    print("    • Health Telemetry Endpoint       : http://127.0.0.1:8000/api/health")
    print("\n[+] Press Ctrl+C to stop the portal server at any time.\n")

    uvicorn.run(
        "backend.app.main:app",
        host="127.0.0.1",
        port=8000,
        reload=False,
        log_level="info"
    )

if __name__ == "__main__":
    main()
