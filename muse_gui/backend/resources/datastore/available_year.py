

from dataclasses import dataclass
from typing import Dict, List

from muse_gui.backend.resources.datastore.base import BaseBackDependents, BaseDatastore, BaseForwardDependents
from muse_gui.backend.resources.datastore.exceptions import KeyAlreadyExists, KeyNotFound
from muse_gui.data_defs.timeslice import AvailableYear

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from . import Datastore

class AvailableYearBackDependents(BaseBackDependents):
    pass

class AvailableYearForwardDependents(BaseForwardDependents):
    commodity: List[str]

class AvailableYearDatastore(BaseDatastore[AvailableYear, AvailableYearBackDependents, AvailableYearForwardDependents]):
    def __init__(self, parent: "Datastore", available_years: List[AvailableYear] = []) -> None:
        self._parent = parent
        self._data = {}
        for available_year in available_years:
            self.create(available_year)


    def create(self, model: AvailableYear) -> AvailableYear:
        return super().create(model, str(model.year))
    
    def read(self, key: str) -> AvailableYear:
        if str(key) not in self._data:
            raise KeyNotFound(str(key), self)
        else:
            return self._data[key]
    
    def update(self, key: str, model: AvailableYear) -> AvailableYear:
        return super().update(key, str(model.year), model)

    def delete(self, key: str) -> None:
        existing = self.read(key)
        forward_deps = self.forward_dependents(existing)
        for commodity_key in forward_deps.commodity:
            try:
                self._parent.commodity.delete(commodity_key)
            except KeyNotFound:
                pass
        self._data.pop(key)
        return None

    def back_dependents(self, model: AvailableYear) -> AvailableYearBackDependents:
        return AvailableYearBackDependents()
    
    def forward_dependents(self, model: AvailableYear) -> AvailableYearForwardDependents:
        commodities = []
        for key, commodity in self._parent.commodity._data.items():
            for price in commodity.commodity_prices.prices:
                if price.time == model.year:
                    commodities.append(key)
        return AvailableYearForwardDependents(
            commodity = commodities
        )

