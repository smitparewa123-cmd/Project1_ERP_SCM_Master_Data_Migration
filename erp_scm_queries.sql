-- ============================================================================
-- ERP SUPPLY CHAIN & INVENTORY SQL SCHEMA + ANALYTICAL QUERIES (P2P & O2C)
-- ============================================================================

-- 1. Inventory Valuation & Reorder Alert Report
SELECT 
    SKU,
    Item_Description,
    Item_Type,
    Current_Stock,
    Reorder_Point,
    Unit_Cost_INR,
    Total_Inventory_Value_INR,
    Replenishment_Status
FROM dim_item_master
ORDER BY Total_Inventory_Value_INR DESC;

-- 2. Gross Margin Analysis on Finished Goods (Order-to-Cash Costing)
SELECT 
    SKU,
    Item_Description,
    Unit_Cost_INR AS Standard_COGS_INR,
    Selling_Price_INR,
    ROUND(Selling_Price_INR - Unit_Cost_INR, 2) AS Gross_Profit_Per_Unit,
    ROUND(((Selling_Price_INR - Unit_Cost_INR) / Selling_Price_INR) * 100, 2) AS Gross_Margin_Pct
FROM dim_item_master
WHERE Item_Type = 'Finished Good';

-- 3. Procure-to-Pay (P2P) Three-Way Match Validation Query
/*
SELECT 
    po.PO_Number,
    po.Vendor_ID,
    po.SKU,
    po.Ordered_Qty,
    gr.Received_Qty,
    inv.Invoiced_Qty,
    CASE 
        WHEN po.Ordered_Qty = gr.Received_Qty AND gr.Received_Qty = inv.Invoiced_Qty THEN 'MATCHED - APPROVE PAYMENT'
        ELSE 'HOLD - QUANTITY DISCREPANCY'
    END AS Three_Way_Match_Status
FROM purchase_orders po
JOIN goods_receipts gr ON po.PO_Number = gr.PO_Number AND po.SKU = gr.SKU
JOIN vendor_invoices inv ON po.PO_Number = inv.PO_Number AND po.SKU = inv.SKU;
*/
