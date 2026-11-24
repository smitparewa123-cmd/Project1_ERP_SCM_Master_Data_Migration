# Supply Chain Inventory, Procurement & Master Data Migration Simulation

An end-to-end **ERP Implementation & Supply Chain Management (SCM)** simulation demonstrating master data cleansing, SQL schema design, **Procure-to-Pay (P2P)** three-way matching, **Order-to-Cash (O2C)** costing/margin analysis, and **User Acceptance Testing (UAT)** documentation.

---

## Business Problem & Objectives
During enterprise ERP implementations (such as Oracle NetSuite, SAP S/4HANA, or Microsoft Dynamics), legacy spreadsheet data often contains duplicate vendor records, negative inventory balances, and unstandardized costing. This project simulates a full-cycle data migration and functional validation workflow across core manufacturing and distribution modules:
1. **Master Data Cleansing & Migration:** Automated ETL pipeline in Python (`pandas` + `sqlite3`) that deduplicates Vendor Master records, flags/corrects negative stock anomalies, and calculates rolled-up Bill of Materials (BOM) standard costs.
2. **Inventory & Reorder Point Management:** Automated stock threshold monitoring (`Current Stock <= Reorder Point`) and inventory valuation reporting.
3. **Procure-to-Pay (P2P) 3-Way Match:** Automated validation comparing Purchase Order (PO), Goods Receipt Note (GRN), and Vendor Invoice quantities to prevent overpayment.
4. **Order-to-Cash (O2C) & Gross Margin Costing:** Dynamic SKU-level COGS lookup and gross margin calculation for Finished Goods sales orders.
5. **UAT & Cutover Readiness:** Structured User Acceptance Testing (UAT) test case log verifying pass/fail criteria prior to Go-Live.

---

## Repository Structure
```text
├── README.md                              # Project documentation & ERP workflow overview
├── raw_legacy_vendors.csv                 # Uncleaned legacy vendor export (with duplicates & nulls)
├── raw_legacy_inventory.csv               # Uncleaned legacy inventory export (with negative stock error)
├── etl_master_data_migration.py           # Python ETL script for cleansing, BOM costing & SQLite load
├── erp_scm_queries.sql                    # SQL queries for Inventory Valuation, COGS & 3-Way Matching
└── ERP_SCM_Master_Data_Workbook.xlsx      # Multi-tab Excel ERP simulation (Inventory, P2P, O2C, UAT)
```

---

## How to Run Locally
1. Clone this repository:
   ```bash
   git clone https://github.com/smitparewa123-cmd/ERP-SCM-Master-Data-Migration.git
   cd ERP-SCM-Master-Data-Migration
   ```
2. Run the Master Data Migration & Cleansing script:
   ```bash
   python etl_master_data_migration.py
   ```
3. Open `ERP_SCM_Master_Data_Workbook.xlsx` to inspect the dynamic Excel formulas (`INDEX/MATCH`, `IF`, `AND`), P2P variance flags, O2C margin analysis, and UAT test sign-off log.
