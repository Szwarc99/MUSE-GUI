import math
from unicodedata import name

import pytest

import muse_gui.backend.data.agent as ag
import muse_gui.backend.data.commodity as com
import muse_gui.backend.data.process as pro
import muse_gui.backend.data.region as reg
import muse_gui.backend.data.sector as sec
import muse_gui.backend.data.timeslice as ts
import muse_gui.backend.resources.datastore.exceptions as exc
from muse_gui.backend.resources.datastore import Datastore


@pytest.fixture
def dstore():
    return Datastore()


@pytest.fixture
def dstore_advanced():
    dstore = Datastore()
    dstore.region.create(reg.Region(name="R1"))
    dstore.sector.create(sec.StandardSector(name="gas", priority=100, type="standard"))
    dstore.sector.create(
        sec.StandardSector(name="power", priority=100, type="standard")
    )
    dstore.sector.create(
        sec.StandardSector(name="residential", priority=100, type="standard")
    )
    for x in range(2000, 2200, 5):
        dstore.available_year.create(ts.AvailableYear(year=x))
    dstore.commodity.create(
        com.Commodity(
            commodity="Electricity",
            commodity_type="Energy",
            commodity_name="electricity",
            c_emission_factor_co2=0.0,
            heat_rate=1.0,
            unit="PJ",
            commodity_prices=[
                com.CommodityPrice(region_name="R1", time=2010, value=14.81481472),
                com.CommodityPrice(region_name="R1", time=2015, value=17.89814806),
                com.CommodityPrice(region_name="R1", time=2020, value=19.5),
                com.CommodityPrice(region_name="R1", time=2025, value=21.93518528),
                com.CommodityPrice(region_name="R1", time=2030, value=26.50925917),
                com.CommodityPrice(region_name="R1", time=2035, value=26.51851861),
                com.CommodityPrice(region_name="R1", time=2040, value=23.85185194),
                com.CommodityPrice(region_name="R1", time=2045, value=23.97222222),
                com.CommodityPrice(region_name="R1", time=2050, value=24.06481472),
                com.CommodityPrice(region_name="R1", time=2055, value=25.3425925),
                com.CommodityPrice(region_name="R1", time=2060, value=25.53703694),
                com.CommodityPrice(region_name="R1", time=2065, value=25.32407417),
                com.CommodityPrice(region_name="R1", time=2070, value=23.36111111),
                com.CommodityPrice(region_name="R1", time=2075, value=22.27777778),
                com.CommodityPrice(region_name="R1", time=2080, value=22.25925917),
                com.CommodityPrice(region_name="R1", time=2085, value=22.17592583),
                com.CommodityPrice(region_name="R1", time=2090, value=22.03703694),
                com.CommodityPrice(region_name="R1", time=2095, value=21.94444444),
                com.CommodityPrice(region_name="R1", time=2100, value=21.39814806),
            ],
            price_unit="MUS$2010/PJ",
        )
    )
    dstore.commodity.create(
        com.Commodity(
            commodity="Gas",
            commodity_type="Energy",
            commodity_name="gas",
            c_emission_factor_co2=0.0,
            heat_rate=1.0,
            unit="PJ",
            commodity_prices=[
                com.CommodityPrice(region_name="R1", time=2010, value=14.81481472),
                com.CommodityPrice(region_name="R1", time=2015, value=17.89814806),
                com.CommodityPrice(region_name="R1", time=2020, value=19.5),
                com.CommodityPrice(region_name="R1", time=2025, value=21.93518528),
                com.CommodityPrice(region_name="R1", time=2030, value=26.50925917),
                com.CommodityPrice(region_name="R1", time=2035, value=26.51851861),
                com.CommodityPrice(region_name="R1", time=2040, value=23.85185194),
                com.CommodityPrice(region_name="R1", time=2045, value=23.97222222),
                com.CommodityPrice(region_name="R1", time=2050, value=24.06481472),
                com.CommodityPrice(region_name="R1", time=2055, value=25.3425925),
                com.CommodityPrice(region_name="R1", time=2060, value=25.53703694),
                com.CommodityPrice(region_name="R1", time=2065, value=25.32407417),
                com.CommodityPrice(region_name="R1", time=2070, value=23.36111111),
                com.CommodityPrice(region_name="R1", time=2075, value=22.27777778),
                com.CommodityPrice(region_name="R1", time=2080, value=22.25925917),
                com.CommodityPrice(region_name="R1", time=2085, value=22.17592583),
                com.CommodityPrice(region_name="R1", time=2090, value=22.03703694),
                com.CommodityPrice(region_name="R1", time=2095, value=21.94444444),
                com.CommodityPrice(region_name="R1", time=2100, value=21.39814806),
            ],
            price_unit="MUS$2010/PJ",
        )
    )

    dstore.commodity.create(
        com.Commodity(
            commodity="Heat",
            commodity_type="Energy",
            commodity_name="heat",
            c_emission_factor_co2=0.0,
            heat_rate=1.0,
            unit="PJ",
            commodity_prices=[
                com.CommodityPrice(region_name="R1", time=2010, value=14.81481472),
                com.CommodityPrice(region_name="R1", time=2015, value=17.89814806),
                com.CommodityPrice(region_name="R1", time=2020, value=19.5),
                com.CommodityPrice(region_name="R1", time=2025, value=21.93518528),
                com.CommodityPrice(region_name="R1", time=2030, value=26.50925917),
                com.CommodityPrice(region_name="R1", time=2035, value=26.51851861),
                com.CommodityPrice(region_name="R1", time=2040, value=23.85185194),
                com.CommodityPrice(region_name="R1", time=2045, value=23.97222222),
                com.CommodityPrice(region_name="R1", time=2050, value=24.06481472),
                com.CommodityPrice(region_name="R1", time=2055, value=25.3425925),
                com.CommodityPrice(region_name="R1", time=2060, value=25.53703694),
                com.CommodityPrice(region_name="R1", time=2065, value=25.32407417),
                com.CommodityPrice(region_name="R1", time=2070, value=23.36111111),
                com.CommodityPrice(region_name="R1", time=2075, value=22.27777778),
                com.CommodityPrice(region_name="R1", time=2080, value=22.25925917),
                com.CommodityPrice(region_name="R1", time=2085, value=22.17592583),
                com.CommodityPrice(region_name="R1", time=2090, value=22.03703694),
                com.CommodityPrice(region_name="R1", time=2095, value=21.94444444),
                com.CommodityPrice(region_name="R1", time=2100, value=21.39814806),
            ],
            price_unit="MUS$2010/PJ",
        )
    )
    dstore.commodity.create(
        com.Commodity(
            commodity="CO2fuelcomsbustion",
            commodity_type="Environmental",
            commodity_name="CO2f",
            c_emission_factor_co2=0.0,
            heat_rate=1.0,
            unit="PJ",
            commodity_prices=[
                com.CommodityPrice(region_name="R1", time=2010, value=14.81481472),
                com.CommodityPrice(region_name="R1", time=2015, value=17.89814806),
                com.CommodityPrice(region_name="R1", time=2020, value=19.5),
                com.CommodityPrice(region_name="R1", time=2025, value=21.93518528),
                com.CommodityPrice(region_name="R1", time=2030, value=26.50925917),
                com.CommodityPrice(region_name="R1", time=2035, value=26.51851861),
                com.CommodityPrice(region_name="R1", time=2040, value=23.85185194),
                com.CommodityPrice(region_name="R1", time=2045, value=23.97222222),
                com.CommodityPrice(region_name="R1", time=2050, value=24.06481472),
                com.CommodityPrice(region_name="R1", time=2055, value=25.3425925),
                com.CommodityPrice(region_name="R1", time=2060, value=25.53703694),
                com.CommodityPrice(region_name="R1", time=2065, value=25.32407417),
                com.CommodityPrice(region_name="R1", time=2070, value=23.36111111),
                com.CommodityPrice(region_name="R1", time=2075, value=22.27777778),
                com.CommodityPrice(region_name="R1", time=2080, value=22.25925917),
                com.CommodityPrice(region_name="R1", time=2085, value=22.17592583),
                com.CommodityPrice(region_name="R1", time=2090, value=22.03703694),
                com.CommodityPrice(region_name="R1", time=2095, value=21.94444444),
                com.CommodityPrice(region_name="R1", time=2100, value=21.39814806),
            ],
            price_unit="MUS$2010/PJ",
        )
    )

    dstore.agent.create(
        ag.Agent(
            name="A1",
            sectors=["gas", "power", "residential"],
            new={
                "R1": ag.AgentData(
                    num=None,
                    objective_1=ag.AgentObjective(
                        objective_type="LCOE", objective_data=1.0, objective_sort=False
                    ),
                    budget=math.inf,
                    share="Agent1",
                    objective_2=None,
                    objective_3=None,
                    search_rule="all",
                    decision_method="singleObj",
                    quantity=1.0,
                    maturity_threshold=-1.0,
                )
            },
            retrofit={
                "R1": ag.AgentData(
                    num=None,
                    objective_1=ag.AgentObjective(
                        objective_type="LCOE", objective_data=1.0, objective_sort=False
                    ),
                    budget=math.inf,
                    share="Agent2",
                    objective_2=None,
                    objective_3=None,
                    search_rule="all",
                    decision_method="singleObj",
                    quantity=1.0,
                    maturity_threshold=-1.0,
                )
            },
        )
    )
    return dstore
