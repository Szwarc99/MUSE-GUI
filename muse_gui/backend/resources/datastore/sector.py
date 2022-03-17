from typing import Dict, List, Union

from .base import BaseDatastore
from muse_gui.backend.data.sector import StandardSector, PresetSector, Sector

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from . import Datastore

class SectorDatastore(BaseDatastore[Sector]):
    def __init__(self, parent: "Datastore", sectors: Union[List[StandardSector], List[PresetSector], List[Sector]] = []) -> None:
        self._parent = parent
        self._data = {}
        for sector in sectors:
            self.create(sector)

    def create(self, model: Sector) -> Sector:
        return super().create(model, model.name)

    def update(self, key: str, model: Sector) -> Sector:
        return super().update(key, model.name, model)

    def forward_dependents(self, model: Sector) -> Dict[str,List[str]]:
        processes = []
        for key, process in self._parent.process._data.items():
            if process.sector == model.name:
                processes.append(key)
        return {
            'process': list(set(processes))
        }



