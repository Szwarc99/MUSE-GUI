from unicodedata import name
from muse_gui.backend.resources.datastore import Datastore
import pytest

@pytest.fixture
def dstore():
    return Datastore()