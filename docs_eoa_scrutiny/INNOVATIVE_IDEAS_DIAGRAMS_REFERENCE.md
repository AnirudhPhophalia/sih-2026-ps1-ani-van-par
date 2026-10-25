# AICTE EoA & Approval Scrutiny Platform: Visual Architecture & Diagrams Reference

> **Document Type:** System Architecture Diagrams, State Machines, Data Pipelines & Technical Visuals Reference  
> **Target System:** AICTE Automated Regulatory Scrutiny & Document Intelligence Platform (AICTE-ARSDIP)  

---

## 1. End-to-End System Context Diagram (C4 Level 1)

```mermaid
graph TB
    subgraph External_Actors [Key Stakeholders]
        Inst[Institution Nodal Officer / Registrar]
        DeskOff[AICTE Desk Scrutiny Officer]
        RegOff[Regional Officer / Competent Authority]
        Comm[Standing Hearing & Inspection Committee]
    end

    subgraph ARSDIP_System [AICTE Regulatory Scrutiny & Document Intelligence Platform]
        Portal[Web Scrutiny Portal & API Gateway]
        Engine[AI Scrutiny & Forensics Intelligence Core]
        Storage[(Encrypted Document Vault & Audit Store)]
    end

    subgraph External_Systems [Government & Issuing Repositories]
        DL[DigiLocker / NAD API]
        LandReg[State Land Records: Bhulekh / AnyRoR]
        Univ[State Affiliating Universities]
        CCA[Controller of Certifying Authorities PKI]
        NIC[NIC SMS & Email Alert Gateway]
    end

    Inst -->|1. Uploads Application & Documents| Portal
    Portal -->|2. Dispatches Processing Tasks| Engine
    Engine -->|3. Fetches Verification Data| External_Systems
    Engine -->|4. Persists Artifacts & Evidence| Storage
    Engine -->|5. Compiles Scrutiny Dossier| Portal
    DeskOff -->|6. Reviews Evidence & Issues Rectification| Portal
    Comm -->|7. Evaluates Contested Findings in Hearing| Portal
    RegOff -->|8. Grants Final Statutory EoA / Rejection| Portal
    Portal -->|9. Dispatches Alerts & Letters| NIC
```

---

## 2. Document Scrutiny State Machine & Lifecycle

```mermaid
stateDiagram-v2
    [*] --> DRAFT : Application Created
    DRAFT --> PRE_SUBMISSION_AUDIT : Institute Initiates Self-Scrubbing
    PRE_SUBMISSION_AUDIT --> DRAFT : Rectifies Self-Detected Deficiencies
    DRAFT --> SUBMITTED : Final Submission & TER Fee Paid
    
    SUBMITTED --> INGESTION_AND_HASHING : Ingestion Pipeline Triggered
    INGESTION_AND_HASHING --> ASYNC_AI_SCRUTINY : Checksum Verified & Stored
    
    state ASYNC_AI_SCRUTINY {
        [*] --> OCR_AND_NER : LayoutLM & PaddleOCR
        OCR_AND_NER --> FORENSIC_TAMPER_CHECK : ELA & Metadata Forensics
        FORENSIC_TAMPER_CHECK --> AUTHORITY_QUERY : DigiLocker & Land APIs
        AUTHORITY_QUERY --> COMPUTER_VISION_CHECK : YOLOv8 Lab & Geotag
        COMPUTER_VISION_CHECK --> RULE_ENGINE_EVALUATION : APH Norms Compliance
        RULE_ENGINE_EVALUATION --> [*] : Compile Dossier
    }

    ASYNC_AI_SCRUTINY --> OFFICER_REVIEW_QUEUE : Scrutiny Dossier Ready
    
    state OFFICER_REVIEW_QUEUE {
        GREEN_QUEUE : Clean Compliance (Risk Score < 10)
        YELLOW_QUEUE : Minor Deficiencies (Risk Score 10-40)
        RED_QUEUE : Critical Discrepancies / Anomalies (Risk Score > 40)
    }

    YELLOW_QUEUE --> RECTIFICATION_NOTICE_ISSUED : 7-Day Cure Notice Dispatched
    RECTIFICATION_NOTICE_ISSUED --> SUBMITTED : Institute Uploads Corrected Docs
    RECTIFICATION_NOTICE_ISSUED --> ESCALATED_HEARING : Cure Window Expired Without Cure
    
    RED_QUEUE --> ESCALATED_HEARING : Referred to Standing Scrutiny Committee
    ESCALATED_HEARING --> PHYSICAL_INSPECTION : Expert Visit Ordered
    PHYSICAL_INSPECTION --> COMPETENT_AUTHORITY_DECISION
    
    GREEN_QUEUE --> REGIONAL_OFFICER_SIGN_OFF : Direct Fast-Track Clearance
    REGIONAL_OFFICER_SIGN_OFF --> EOA_GRANTED : Digitally Signed EoA Issued
    
    COMPETENT_AUTHORITY_DECISION --> EOA_GRANTED : Compliance Established
    COMPETENT_AUTHORITY_DECISION --> EOA_REJECTED_OR_PENALIZED : Statutory Rejection
    
    EOA_GRANTED --> [*]
    EOA_REJECTED_OR_PENALIZED --> [*]
```

---

## 3. Computer Vision & Geotag Verification Architecture

```mermaid
flowchart LR
    subgraph Input_Media [Institution Evidence Media]
        IMG1[High-Res Lab Photos]
        IMG2[Classroom & Workshop Photos]
        EXIF_DATA[Embedded EXIF GPS & Timestamp]
    end

    subgraph Spatial_Verifier [Spatial Verification Engine]
        GEO_EXT[EXIF Extractor]
        GEOFENCE[Campus GeoJSON Polygon Boundary]
        RAY_CAST[Ray-Casting Point-in-Polygon Check]
    end

    subgraph Vision_Model [Computer Vision Inference Pipeline]
        YOLO[YOLOv8x Deep Object Detector]
        OBJ_FILTER[Instructional Asset Filter]
        TALLY[Automated Asset Counter]
    end

    subgraph APH_Rule_Tally [Regulatory Benchmark Tally]
        FORM_CLAIM[Declared Terminal Intake Count]
        COMP_CALC[FSR / Terminal Ratio Benchmark: 1:4]
        RESULT_GEN[Visual Compliance Report Generator]
    end

    IMG1 & IMG2 --> YOLO
    IMG1 & IMG2 --> GEO_EXT
    EXIF_DATA --> GEO_EXT
    
    GEO_EXT --> RAY_CAST
    GEOFENCE --> RAY_CAST
    
    YOLO --> OBJ_FILTER --> TALLY
    
    TALLY & FORM_CLAIM & COMP_CALC & RAY_CAST --> RESULT_GEN
    
    RESULT_GEN --> OUT1[Compliance: Validated Inside Campus & PC Count Verified]
    RESULT_GEN --> OUT2[Alert: Photo Outside Boundary or Deficit PCs]
```

---

## 4. Multi-Modal Document Forensics & ELA Architecture

```
                  ┌────────────────────────────────────────┐
                  │ Scanned Document / Certificate (PDF)   │
                  └───────────────────┬────────────────────┘
                                      │
                 ┌────────────────────┴────────────────────┐
                 ▼                                         ▼
   ┌───────────────────────────┐             ┌───────────────────────────┐
   │    Raster Conversion      │             │  PDF Stream & Byte Parser │
   │    (300 DPI Rendering)    │             │ (PyMuPDF / pdfminer.six)  │
   └─────────────┬─────────────┘             └─────────────┬─────────────┘
                 │                                         │
        ┌────────┴────────┐                       ┌────────┴────────┐
        ▼                 ▼                       ▼                 ▼
 ┌──────────────┐  ┌──────────────┐        ┌──────────────┐  ┌──────────────┐
 │ Error Level  │  │ Resampling & │        │   Metadata   │  │ Embedded Font│
 │ Analysis     │  │ Copy-Move    │        │ Authoring    │  │ Discrepancy  │
 │ (ELA) Engine │  │ pHash Engine │        │ Tool Audit   │  │ Layer Audit  │
 └──────┬───────┘  └──────┬───────┘        └──────┬───────┘  └──────┬───────┘
        │                 │                       │                 │
        └────────┬────────┴───────────────────────┴────────┬────────┘
                 │                                         │
                 ▼                                         ▼
   ┌─────────────────────────────────────────────────────────────┐
   │ Forensic Aggregator & Explainability Scoring Engine         │
   │ - Generates Visual Tamper Heatmaps (Red Glow Overlay)       │
   │ - Identifies Forensic Alteration Confidence Score           │
   │ - Localizes Dynamic Bounding Boxes (x1, y1, x2, y2)         │
   └──────────────────────────────┬──────────────────────────────┘
                                  │
                                  ▼
   ┌─────────────────────────────────────────────────────────────┐
   │ Split-Screen Scrutiny Dossier (Evidence-Linked Findings)    │
   └─────────────────────────────────────────────────────────────┘
```

---

## 5. Entity-Relationship Model (Data Schema ERD)

```mermaid
erDiagram
    INSTITUTION ||--o{ APPLICATION : submits
    APPLICATION ||--o{ APPLICATION_DOCUMENT : contains
    APPLICATION_DOCUMENT ||--o{ EXTRACTED_ENTITY : yields
    APPLICATION_DOCUMENT ||--o{ FORENSIC_ANOMALY : triggers
    APPLICATION_DOCUMENT ||--o{ AUTHORITY_VERIFICATION : initiates
    APPLICATION ||--o{ COMPLIANCE_CHECK : evaluated_by
    APPLICATION ||--o{ AUDIT_EVENT : records

    INSTITUTION {
        uuid id PK
        string aicte_permanent_id UK
        string institution_name
        string trust_name
        string region
        string state
        string urban_rural_status
        decimal campus_latitude
        decimal campus_longitude
    }

    APPLICATION {
        uuid id PK
        uuid institution_id FK
        string academic_year
        string application_category
        string current_status
        decimal ai_risk_score
        uuid scrutiny_officer_id
    }

    APPLICATION_DOCUMENT {
        uuid id PK
        uuid application_id FK
        string document_category
        string s3_storage_uri
        string sha256_hash
        string perceptual_hash
    }

    FORENSIC_ANOMALY {
        uuid id PK
        uuid document_id FK
        string anomaly_type
        string severity
        decimal confidence_score
        string explanation
        jsonb bounding_box_json
        string evidence_heatmap_uri
    }

    AUTHORITY_VERIFICATION {
        uuid id PK
        uuid document_id FK
        string authority_name
        string query_reference_no
        string verification_status
        jsonb authority_response_payload
    }

    COMPLIANCE_CHECK {
        uuid id PK
        uuid application_id FK
        string rule_code
        string required_value
        string submitted_value
        string compliance_status
    }
```
