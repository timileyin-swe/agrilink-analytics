CREATE TABLE IF NOT EXISTS suppliers (supplier_id TEXT PRIMARY KEY, name TEXT NOT NULL, state TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS buyers (buyer_id TEXT PRIMARY KEY, name TEXT NOT NULL, location TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS produce (produce_id TEXT PRIMARY KEY, name TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS deliveries (
 delivery_id TEXT PRIMARY KEY,
 supplier_id TEXT NOT NULL REFERENCES suppliers(supplier_id),
 buyer_id TEXT NOT NULL REFERENCES buyers(buyer_id),
 produce_id TEXT NOT NULL REFERENCES produce(produce_id),
 pickup_date DATE NOT NULL,
 delivery_date DATE NOT NULL,
 harvested_kg NUMERIC(12,2) NOT NULL CHECK (harvested_kg > 0),
 delivered_kg NUMERIC(12,2) NOT NULL CHECK (delivered_kg >= 0),
 spoiled_kg NUMERIC(12,2) NOT NULL CHECK (spoiled_kg >= 0),
 CHECK (delivery_date >= pickup_date),
 CHECK (delivered_kg + spoiled_kg <= harvested_kg)
);
