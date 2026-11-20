# AgriLink Supply & Loss Analytics

A portfolio project to study tomato and pepper delivery losses. All sample data is synthetic and must not be presented as observed business results.

## First milestone

Build a reproducible delivery dataset, validate it with Python, and load it into PostgreSQL. Then create a Power BI report with operations, spoilage, and supplier pages. Add a small FastAPI service after the data model and report are clear.

## Proposed data model

- `suppliers`: supplier ID, name, state
- `buyers`: buyer ID, name, location
- `produce`: produce ID, name
- `deliveries`: delivery ID, supplier ID, buyer ID, produce ID, pickup date, delivery date, harvested kg, delivered kg, spoiled kg

Rules: IDs are unique; quantities are nonnegative; delivered plus spoiled cannot exceed harvested; delivery date cannot precede pickup date. Define loss rate as spoiled kg divided by harvested kg, with zero harvest handled as blank.

## Power BI report

1. Operations: total harvested, delivered, spoiled, and delivery count by month.
2. Spoilage: loss rate by produce, supplier, and location.
3. Supplier performance: delivered volume and loss rate, with filters for dates and produce.

Keep the raw data, Python validation, SQL schema, report file, screenshots, and a short explanation of each metric in this repository. Clearly label every chart as based on synthetic sample data.

## First exercise

Explain why a delivery with 100 kg harvested, 80 kg delivered, and 25 kg spoiled must be rejected.

## Run the first milestone

Install Python 3.12 and PostgreSQL. In PowerShell:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pytest -q
```

Create an empty PostgreSQL database, then run these files in order with `psql`:

```powershell
psql -d agrilink_analytics -f schema.sql
psql -d agrilink_analytics -f sample_dimensions.sql
.\.venv\Scripts\python.exe import_deliveries.py data/sample_deliveries.csv "postgresql://localhost/agrilink_analytics"
```

Adjust the connection URL to your PostgreSQL username and credentials. Repeating the import skips existing delivery IDs. The whole import uses one transaction; a missing supplier or buyer rejects the batch. `sample_dimensions.sql` contains fictional names. The six delivery records are synthetic examples, not AgriLink findings.

## Query the analytics view

After importing the sample, run `psql -d agrilink_analytics -f analytics.sql`.
The `delivery_analytics` view joins deliveries to their supplier, buyer, and
produce names and calculates `spoilage_percent`. For example:

```sql
SELECT produce_name, SUM(harvested_kg) AS harvested_kg,
       SUM(spoiled_kg) AS spoiled_kg,
       ROUND(100 * SUM(spoiled_kg) / NULLIF(SUM(harvested_kg), 0), 2)
           AS spoilage_percent
FROM delivery_analytics
GROUP BY produce_name
ORDER BY produce_name;
```

`other_loss_kg` is the remaining difference between harvested, delivered,
and spoiled amounts. It is not automatically spoilage. Power BI should connect
to PostgreSQL and use the delivery view for exploration; the final report will
use a documented star model. Keep credentials in your local connection settings,
not in Git.
