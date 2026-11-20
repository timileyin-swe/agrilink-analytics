-- One row per delivery, suitable for Power BI's central fact table.
CREATE OR REPLACE VIEW delivery_analytics AS
SELECT d.delivery_id, d.pickup_date, d.delivery_date,
       d.harvested_kg, d.delivered_kg, d.spoiled_kg,
       d.harvested_kg - d.delivered_kg - d.spoiled_kg AS other_loss_kg,
       ROUND(100 * d.spoiled_kg / NULLIF(d.harvested_kg, 0), 2) AS spoilage_percent,
       s.supplier_id, s.name AS supplier_name, s.state AS supplier_state,
       b.buyer_id, b.name AS buyer_name, b.location AS buyer_location,
       p.produce_id, p.name AS produce_name
FROM deliveries d
JOIN suppliers s USING (supplier_id)
JOIN buyers b USING (buyer_id)
JOIN produce p USING (produce_id);
