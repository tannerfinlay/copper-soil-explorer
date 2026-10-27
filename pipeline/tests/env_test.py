import pytest

def f():
  raise SystemExit(1)

class TestEnv:

  def test_one(self):
    x = "this"
    assert "h" in x

  def test_two(self):
    with pytest.raises(SystemExit):
      f()
