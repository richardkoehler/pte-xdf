"""Tests for xdf.py"""
import pathlib

import numpy as np
import pte_xdf

_data_dir = pathlib.Path(__file__).parent.parent / "data"


def test_read_emg() -> None:
    """Test reading example EMG data."""
    fname = _data_dir / "test_read_emg.xdf"
    raw = pte_xdf.read_raw_xdf(fname, stream_picks=1, verbose=True)
    data = raw.get_data()
    assert isinstance(data, np.ndarray)
    assert data.shape == (34, 167008)


if __name__ == "__main__":
    test_read_emg()
