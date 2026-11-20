from pathlib import Path

import pytest

from import_deliveries import FIELDS, validate_rows


def write_sample(tmp_path, *records):
    path = tmp_path / 'data.csv'
    path.write_text(','.join(FIELDS) + '\n' + '\n'.join(records) + '\n', encoding='utf-8')
    return path


def test_sample_data_is_valid():
    rows = validate_rows(Path('data/sample_deliveries.csv'))
    assert len(rows) == 6
    assert sum(row['spoiled_kg'] for row in rows) == 74


@pytest.mark.parametrize('record', [
    'D1,S1,B1,P1,2026-01-02,2026-01-01,100,80,10',
    'D1,S1,B1,P1,2026-01-01,2026-01-02,100,80,25',
    'D1,S1,B1,P1,2026-01-01,2026-01-02,100,-1,10',
    'D1,S1,B1,P1,2026-01-01,2026-01-02,NaN,1,1',
    'D1,S1,B1,P1,2026-01-01,2026-01-02,0,0,0',
])
def test_invalid_delivery_is_rejected(tmp_path, record):
    with pytest.raises(ValueError):
        validate_rows(write_sample(tmp_path, record))


def test_duplicate_id_is_rejected(tmp_path):
    record = 'D1,S1,B1,P1,2026-01-01,2026-01-02,100,80,10'
    with pytest.raises(ValueError, match='duplicate'):
        validate_rows(write_sample(tmp_path, record, record))
