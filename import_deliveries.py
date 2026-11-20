from __future__ import annotations

import csv
import sys
from datetime import date
from decimal import Decimal, InvalidOperation
from pathlib import Path

FIELDS = ('delivery_id', 'supplier_id', 'buyer_id', 'produce_id', 'pickup_date', 'delivery_date', 'harvested_kg', 'delivered_kg', 'spoiled_kg')


def validate_rows(path: Path) -> list[dict]:
    with path.open(newline='', encoding='utf-8-sig') as source:
        reader = csv.DictReader(source)
        if reader.fieldnames != list(FIELDS):
            raise ValueError(f'Expected columns: {", ".join(FIELDS)}')
        rows = []
        seen = set()
        for line, raw in enumerate(reader, start=2):
            if not all(raw.get(key, '').strip() for key in FIELDS):
                raise ValueError(f'Line {line}: missing value')
            if raw['delivery_id'] in seen:
                raise ValueError(f'Line {line}: duplicate delivery_id')
            seen.add(raw['delivery_id'])
            try:
                pickup = date.fromisoformat(raw['pickup_date'])
                delivery = date.fromisoformat(raw['delivery_date'])
                amounts = [Decimal(raw[key]) for key in FIELDS[-3:]]
            except (ValueError, InvalidOperation) as exc:
                raise ValueError(f'Line {line}: invalid date or quantity') from exc
            if not all(amount.is_finite() for amount in amounts):
                raise ValueError(f'Line {line}: quantity must be finite')
            harvested, delivered, spoiled = amounts
            if delivery < pickup or harvested <= 0 or delivered < 0 or spoiled < 0 or delivered + spoiled > harvested:
                raise ValueError(f'Line {line}: invalid delivery balance or dates')
            rows.append({**raw, 'pickup_date': pickup, 'delivery_date': delivery,
                         'harvested_kg': harvested, 'delivered_kg': delivered, 'spoiled_kg': spoiled})
        return rows


def main() -> None:
    import psycopg
    if len(sys.argv) != 3:
        raise SystemExit('Usage: python import_deliveries.py DATA.csv POSTGRES_URL')
    rows = validate_rows(Path(sys.argv[1]))
    with psycopg.connect(sys.argv[2]) as connection:
        with connection.cursor() as cursor:
            for row in rows:
                cursor.execute('''INSERT INTO deliveries
                    (delivery_id,supplier_id,buyer_id,produce_id,pickup_date,delivery_date,harvested_kg,delivered_kg,spoiled_kg)
                    VALUES (%(delivery_id)s,%(supplier_id)s,%(buyer_id)s,%(produce_id)s,%(pickup_date)s,%(delivery_date)s,%(harvested_kg)s,%(delivered_kg)s,%(spoiled_kg)s)
                    ON CONFLICT (delivery_id) DO NOTHING''', row)
    print(f'Validated {len(rows)} deliveries; new IDs imported.')


if __name__ == '__main__':
    main()
