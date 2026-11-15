import os
import sys

import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
for p in (os.path.join(HERE, "..", ".."), os.path.join(HERE, "..")):
    p = os.path.abspath(p)
    if p not in sys.path:
        sys.path.insert(0, p)

from libv import v2


@pytest.fixture(autouse=True)
def setup():
    v2.reset()
