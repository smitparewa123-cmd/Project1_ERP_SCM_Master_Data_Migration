import pandas as pd
import sqlite3

def run_erp_migration():
    print("Starting ERP Master Data Migration & Cleansing Pipeline...")
    vendors = pd.read_csv("raw_legacy_vendors.csv")
    items = pd.read_csv("raw_legacy_inventory.csv")
    audit_log = []

    initial_v = len(vendors)
    vendors["Vendor_Name"] = vendors["Vendor_Name"].astype(str).str.strip()
    vendors = vendors[vendors["Vendor_Name"] != "nan"]
    vendors = vendors.drop_duplicates(subset=["Vendor_ID"], keep="first")
    audit_log.append(f"Vendor Master: Removed {initial_v - len(vendors)} duplicate/null records.")

    neg_stock = items[items["Current_Stock"] < 0]["SKU"].tolist()
    if neg_stock:
        audit_log.append(f"Item Master Anomaly Flagged & Corrected: Negative stock on {neg_stock} reset to 0.")
        items.loc[items["Current_Stock"] < 0, "Current_Stock"] = 0

    cost_map = items.set_index("SKU")["Unit_Cost_INR"].to_dict()
    fg100_cost = round(0.75*cost_map["RM-001"] + 0.25*cost_map["RM-002"] + 1*cost_map["PKG-01"] + (1/12)*cost_map["PKG-02"], 2)
    fg200_cost = round(0.80*cost_map["RM-001"] + 0.20*cost_map["RM-002"] + 1*cost_map["PKG-01"] + (1/12)*cost_map["PKG-02"] + 25.0, 2)

    items.loc[items["SKU"] == "FG-100", "Unit_Cost_INR"] = fg100_cost
    items.loc[items["SKU"] == "FG-200", "Unit_Cost_INR"] = fg200_cost
    items["Total_Inventory_Value_INR"] = (items["Unit_Cost_INR"] * items["Current_Stock"]).round(2)
    items["Replenishment_Status"] = items.apply(
        lambda r: "REORDER REQUIRED" if r["Current_Stock"] <= r["Reorder_Point"] else "OK", axis=1
    )

    conn = sqlite3.connect("erp_staging.db")
    vendors.to_sql("dim_vendor_master", conn, if_exists="replace", index=False)
    items.to_sql("dim_item_master", conn, if_exists="replace", index=False)
    conn.close()

    print("Migration Complete! Audit Log:")
    for entry in audit_log:
        print(" -", entry)
    return vendors, items, audit_log

if __name__ == "__main__":
    run_erp_migration()
