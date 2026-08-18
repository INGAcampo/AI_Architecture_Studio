from models.structural.column import Column

def test_column_volume():
    c = Column(width=0.40, depth=0.40, height=3.00)
    assert round(c.volume, 2) == 0.48
