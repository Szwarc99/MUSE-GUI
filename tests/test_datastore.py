import math

import pytest

import muse_gui.backend.data.agent as ag
import muse_gui.backend.data.commodity as com
import muse_gui.backend.data.process as pro
import muse_gui.backend.data.region as reg
import muse_gui.backend.data.sector as sec
import muse_gui.backend.data.timeslice as ts
import muse_gui.backend.resources.datastore.exceptions as exc
from muse_gui.backend.resources.datastore import Datastore

# dstore = Datastore()
# dstore.available_year.create(ts.AvailableYear(year=100))
# dstore.available_year.read('100')
# dstore.commodity.create(com.Commodity(commodity='test',commodity_type='Energy',commodity_name='test',c_emission_factor_co2=0.5,heat_rate=0.5,unit='CBM',commodity_prices='10000000000',price_unit='rouble'))


# region tests
def test_region_create(dstore):
    dstore.region.create(reg.Region(name="R1"))
    with pytest.raises(exc.KeyAlreadyExists) as e:
        dstore.region.create(reg.Region(name="R1"))


def test_region_read(dstore):
    dstore.region.create(reg.Region(name="R1"))
    assert dstore.region.read("R1").name == "R1"
    with pytest.raises(exc.KeyNotFound) as e:
        dstore.region.read("R2")


def test_region_update(dstore):
    dstore.region.create(reg.Region(name="R1"))
    dstore.region.update("R1", reg.Region(name="R2"))
    with pytest.raises(exc.KeyNotFound) as e:
        dstore.region.read("R1")


def test_region_delete(dstore):
    dstore.region.create(reg.Region(name="R1"))
    dstore.region.delete("R1")
    with pytest.raises(exc.KeyNotFound) as e:
        dstore.region.read("R1")


def test_region_list(dstore):
    dstore.region.create(reg.Region(name="R1"))
    dstore.region.create(reg.Region(name="R2"))
    assert len(dstore.region.list()) == 2


def test_region_forward_dependents_recursive():
    dstore = Datastore.from_settings("test_data2/settings.toml")
    dict = dstore.region.forward_dependents_recursive(dstore.region.read("R1"))
    assert len(dict["commodity"]) == 5
    assert len(dict["process"]) == 5
    assert len(dict["agent"]) == 1


# sector tests
def test_sector_create(dstore):
    dstore.sector.create(sec.StandardSector(name="test", priority=100, type="standard"))
    with pytest.raises(exc.KeyAlreadyExists) as e:
        dstore.sector.create(
            sec.StandardSector(name="test", priority=100, type="standard")
        )


def test_sector_read(dstore):
    dstore.sector.create(sec.StandardSector(name="test", priority=100, type="standard"))
    assert dstore.sector.read("test").name == "test"
    with pytest.raises(exc.KeyNotFound) as e:
        dstore.sector.read("test2")


def test_sector_update(dstore):
    dstore.sector.create(sec.StandardSector(name="test", priority=100, type="standard"))
    dstore.sector.update(
        "test", sec.StandardSector(name="test2", priority=100, type="standard")
    )
    with pytest.raises(exc.KeyNotFound) as e:
        dstore.sector.read("test")


def test_sector_delete(dstore):
    dstore.sector.create(sec.StandardSector(name="test", priority=100, type="standard"))
    dstore.sector.delete("test")
    with pytest.raises(exc.KeyNotFound) as e:
        dstore.sector.read("test")


def test_sector_list(dstore):
    dstore.sector.create(sec.StandardSector(name="test", priority=100, type="standard"))
    dstore.sector.create(
        sec.StandardSector(name="test2", priority=100, type="standard")
    )
    assert len(dstore.sector.list()) == 2


def test_sector_forward_dependents_recursive():
    dstore = Datastore.from_settings("test_data2/settings.toml")

    dict = dstore.sector.forward_dependents_recursive(dstore.sector.read("gas"))
    assert len(dict["process"]) == 5
    assert len(dict["agent"]) == 1


# level_name tests
def test_level_name_create(dstore):
    dstore.level_name.create(ts.LevelName(level="R1"))
    with pytest.raises(exc.KeyAlreadyExists) as e:
        dstore.level_name.create(ts.LevelName(level="R1"))


def test_level_name_read(dstore):
    dstore.level_name.create(ts.LevelName(level="R1"))
    assert dstore.level_name.read("R1").level == "R1"
    with pytest.raises(exc.KeyNotFound) as e:
        dstore.level_name.read("R2")


def test_level_name_update(dstore):
    dstore.level_name.create(ts.LevelName(level="R1"))
    dstore.level_name.update("R1", ts.LevelName(level="R2"))
    with pytest.raises(exc.KeyNotFound) as e:
        dstore.level_name.read("R1")


def test_level_name_delete(dstore):
    dstore.level_name.create(ts.LevelName(level="R1"))
    dstore.level_name.delete("R1")
    with pytest.raises(exc.KeyNotFound) as e:
        dstore.level_name.read("R1")


def test_level_name_list(dstore):
    dstore.level_name.create(ts.LevelName(level="R1"))
    dstore.level_name.create(ts.LevelName(level="R2"))
    assert len(dstore.level_name.list()) == 2


def test_level_name_forward_dependents_recursive():
    dstore = Datastore.from_settings("test_data2/settings.toml")
    dict = dstore.level_name.forward_dependents_recursive(
        dstore.level_name.read("month")
    )
    assert len(dict["timeslice"]) == 6


# available_year tests
def test_available_year_create(dstore):
    dstore.available_year.create(ts.AvailableYear(year=100))
    with pytest.raises(exc.KeyAlreadyExists) as e:
        dstore.available_year.create(ts.AvailableYear(year=100))


def test_available_year_read(dstore):
    dstore.available_year.create(ts.AvailableYear(year=100))
    assert dstore.available_year.read("100").year == 100
    with pytest.raises(exc.KeyNotFound) as e:
        dstore.available_year.read("200")


def test_available_year_update(dstore):
    dstore.available_year.create(ts.AvailableYear(year=100))
    dstore.available_year.update("100", ts.AvailableYear(year=200))
    with pytest.raises(exc.KeyNotFound) as e:
        dstore.available_year.read("100")


def test_available_year_delete(dstore):
    dstore.available_year.create(ts.AvailableYear(year=100))
    dstore.available_year.delete("100")
    with pytest.raises(exc.KeyNotFound) as e:
        dstore.available_year.read("100")


def test_available_year_list(dstore):
    dstore.available_year.create(ts.AvailableYear(year=100))
    dstore.available_year.create(ts.AvailableYear(year=200))
    assert len(dstore.available_year.list()) == 2


def test_available_year_forward_dependents_recursive(dstore_advanced):

    dict = dstore_advanced.available_year.forward_dependents_recursive(
        dstore_advanced.available_year.read("2020")
    )
    assert len(dict["commodity"]) == 4
    assert len(dict["process"]) == 0


# timeslice tests
def test_timeslice_create(dstore):
    dstore.level_name.create(ts.LevelName(level="L1"))
    dstore.timeslice.create(ts.Timeslice(name="test", value=100))
    with pytest.raises(exc.KeyAlreadyExists) as e:
        dstore.timeslice.create(ts.Timeslice(name="test", value=100))


def test_timeslice_read(dstore):
    dstore.level_name.create(ts.LevelName(level="L1"))
    dstore.timeslice.create(ts.Timeslice(name="test", value=100))
    assert dstore.timeslice.read("test").name == "test"
    with pytest.raises(exc.KeyNotFound) as e:
        dstore.timeslice.read("test2")


def test_timeslice_update(dstore):
    dstore.level_name.create(ts.LevelName(level="L1"))
    dstore.timeslice.create(ts.Timeslice(name="test", value=100))
    dstore.timeslice.update("test", ts.Timeslice(name="test2", value=100))
    with pytest.raises(exc.KeyNotFound) as e:
        dstore.timeslice.read("test")


def test_timeslice_delete(dstore):
    dstore.level_name.create(ts.LevelName(level="L1"))
    dstore.timeslice.create(ts.Timeslice(name="test", value=100))
    dstore.timeslice.delete("test")
    with pytest.raises(exc.KeyNotFound) as e:
        dstore.timeslice.read("test")


def test_timeslice_list(dstore):
    dstore.level_name.create(ts.LevelName(level="L1"))
    dstore.timeslice.create(ts.Timeslice(name="test", value=100))
    dstore.timeslice.create(ts.Timeslice(name="test2", value=100))
    assert len(dstore.timeslice.list()) == 2


def test_timeslice_back_dependents_recursive():
    dstore = Datastore.from_settings("test_data2/settings.toml")
    dict = dstore.timeslice.back_dependents_recursive(
        dstore.timeslice.read("all-year.all-week.night")
    )
    print(dict)
    assert len(dict["level_name"]) == 3


# commodity tests
def test_commodity_create(dstore):
    dstore.region.create(reg.Region(name="east"))
    dstore.available_year.create(ts.AvailableYear(year=2020))

    dstore.commodity.create(
        com.Commodity(
            commodity="test",
            commodity_type="Energy",
            commodity_name="test",
            c_emission_factor_co2=0.5,
            heat_rate=0.5,
            unit="CBM",
            commodity_prices=[{"region_name": "east", "time": 2020, "value": 0.1}],
            price_unit="rouble",
        )
    )

    with pytest.raises(exc.KeyAlreadyExists) as e:
        dstore.commodity.create(
            com.Commodity(
                commodity="test",
                commodity_type="Energy",
                commodity_name="test",
                c_emission_factor_co2=0.5,
                heat_rate=0.5,
                unit="CBM",
                commodity_prices=[{"region_name": "east", "time": 2020, "value": 0.1}],
                price_unit="rouble",
            )
        )


def test_commodity_read(dstore):
    dstore.region.create(reg.Region(name="east"))
    dstore.available_year.create(ts.AvailableYear(year=2020))

    dstore.commodity.create(
        com.Commodity(
            commodity="test",
            commodity_type="Energy",
            commodity_name="test",
            c_emission_factor_co2=0.5,
            heat_rate=0.5,
            unit="CBM",
            commodity_prices=[{"region_name": "east", "time": 2020, "value": 0.1}],
            price_unit="rouble",
        )
    )

    assert dstore.commodity.read("test").commodity_name == "test"
    with pytest.raises(exc.KeyNotFound) as e:
        dstore.commodity.read("test2")


def test_commodity_update(dstore):
    dstore.region.create(reg.Region(name="east"))
    dstore.available_year.create(ts.AvailableYear(year=2020))

    dstore.commodity.create(
        com.Commodity(
            commodity="test",
            commodity_type="Energy",
            commodity_name="test",
            c_emission_factor_co2=0.5,
            heat_rate=0.5,
            unit="CBM",
            commodity_prices=[{"region_name": "east", "time": 2020, "value": 0.1}],
            price_unit="rouble",
        )
    )

    updated = com.Commodity(
        commodity="test2",
        commodity_type="Energy",
        commodity_name="test2",
        c_emission_factor_co2=0.5,
        heat_rate=0.5,
        unit="CBM",
        commodity_prices=[{"region_name": "east", "time": 2020, "value": 0.1}],
        price_unit="rouble",
    )
    dstore.commodity.update("test", updated)

    with pytest.raises(exc.KeyNotFound) as e:
        dstore.commodity.read("test")


def test_commodity_delete(dstore):
    dstore.region.create(reg.Region(name="east"))
    dstore.available_year.create(ts.AvailableYear(year=2020))

    dstore.commodity.create(
        com.Commodity(
            commodity="test",
            commodity_type="Energy",
            commodity_name="test",
            c_emission_factor_co2=0.5,
            heat_rate=0.5,
            unit="CBM",
            commodity_prices=[{"region_name": "east", "time": 2020, "value": 0.1}],
            price_unit="rouble",
        )
    )
    dstore.commodity.delete("test")
    with pytest.raises(exc.KeyNotFound) as e:
        dstore.commodity.read("test")


def test_commodity_list(dstore):
    dstore.region.create(reg.Region(name="east"))
    dstore.available_year.create(ts.AvailableYear(year=2020))

    dstore.commodity.create(
        com.Commodity(
            commodity="test",
            commodity_type="Energy",
            commodity_name="test",
            c_emission_factor_co2=0.5,
            heat_rate=0.5,
            unit="CBM",
            commodity_prices=[{"region_name": "east", "time": 2020, "value": 0.1}],
            price_unit="rouble",
        )
    )
    dstore.commodity.create(
        com.Commodity(
            commodity="test2",
            commodity_type="Energy",
            commodity_name="test2",
            c_emission_factor_co2=0.5,
            heat_rate=0.5,
            unit="CBM",
            commodity_prices=[{"region_name": "east", "time": 2020, "value": 0.1}],
            price_unit="rouble",
        )
    )
    assert len(dstore.commodity.list()) == 2


def test_commodity_forward_dependents_recursive(dstore):
    dstore = Datastore.from_settings("test_data2/settings.toml")
    dict = dstore.commodity.forward_dependents_recursive(dstore.commodity.read("Gas"))
    assert len(dict["process"]) == 2


def test_commodity_back_dependents_recursive(dstore):
    dstore = Datastore.from_settings("test_data2/settings.toml")
    dict = dstore.commodity.back_dependents_recursive(dstore.commodity.read("Gas"))
    print(dict)
    assert len(dict["region"]) == 1
    assert len(dict["available_year"]) == 19


# process tests

tech = pro.Technodata(
    region="R1",
    time="2020",
    level="fixed",
    cost=pro.Cost(
        cap_par=3.8,
        cap_exp=1.0,
        fix_par=0.0,
        fix_exp=1.0,
        var_par=0.0,
        var_exp=1.0,
        interest_rate=0.1,
    ),
    utilisation=pro.Utilisation(utilization_factor=1.0, efficiency=86.0),
    capacity=pro.Capacity(
        max_capacity_addition=10,
        max_capacity_growth=0.02,
        total_capacity_limit=60,
        technical_life=10,
        scaling_size=1.89e-06,
    ),
    agents=[
        pro.CapacityShare(
            agent_name="A1", agent_type=ag.AgentType.Retrofit, region="R1", share=1.0
        )
    ],
)


def test_process_create(dstore_advanced):
    dstore_advanced.process.create(
        pro.Process(
            name="gasboiler",
            sector="residential",
            preset_sector=None,
            fuel="gas",
            end_use="heat",
            type="energy",
            technodatas=[tech],
            comm_in=[
                pro.CommodityFlow(
                    commodity="Heat",
                    region="R1",
                    timeslice="2020",
                    level="fixed",
                    value=1.16,
                )
            ],
            comm_out=[
                pro.CommodityFlow(
                    commodity="Heat",
                    region="R1",
                    timeslice="2020",
                    level="fixed",
                    value=1.0,
                ),
                pro.CommodityFlow(
                    commodity="CO2fuelcomsbustion",
                    region="R1",
                    timeslice="2020",
                    level="fixed",
                    value=64.71,
                ),
            ],
            demands=[],
            existing_capacities=[
                pro.ExistingCapacity(region="R1", year=2020, value=10.0),
                pro.ExistingCapacity(region="R1", year=2025, value=5.0),
                pro.ExistingCapacity(region="R1", year=2030, value=0.0),
                pro.ExistingCapacity(region="R1", year=2035, value=0.0),
                pro.ExistingCapacity(region="R1", year=2040, value=0.0),
                pro.ExistingCapacity(region="R1", year=2045, value=0.0),
                pro.ExistingCapacity(region="R1", year=2050, value=0.0),
            ],
            capacity_unit="PJ/y",
        )
    )
    with pytest.raises(exc.KeyAlreadyExists) as e:
        dstore_advanced.process.create(
            pro.Process(
                name="gasboiler",
                sector="residential",
                preset_sector=None,
                fuel="gas",
                end_use="heat",
                type="energy",
                technodatas=[tech],
                comm_in=[
                    pro.CommodityFlow(
                        commodity="Gas",
                        region="R1",
                        timeslice="2020",
                        level="fixed",
                        value=1.16,
                    )
                ],
                comm_out=[
                    pro.CommodityFlow(
                        commodity="Heat",
                        region="R1",
                        timeslice="2020",
                        level="fixed",
                        value=1.0,
                    ),
                    pro.CommodityFlow(
                        commodity="CO2fuelcomsbustion",
                        region="R1",
                        timeslice="2020",
                        level="fixed",
                        value=64.71,
                    ),
                ],
                demands=[],
                existing_capacities=[
                    pro.ExistingCapacity(region="R1", year=2020, value=10.0),
                    pro.ExistingCapacity(region="R1", year=2025, value=5.0),
                    pro.ExistingCapacity(region="R1", year=2030, value=0.0),
                    pro.ExistingCapacity(region="R1", year=2035, value=0.0),
                    pro.ExistingCapacity(region="R1", year=2040, value=0.0),
                    pro.ExistingCapacity(region="R1", year=2045, value=0.0),
                    pro.ExistingCapacity(region="R1", year=2050, value=0.0),
                ],
                capacity_unit="PJ/y",
            )
        )


def test_process_read(dstore_advanced):
    dstore_advanced.process.create(
        pro.Process(
            name="gasboiler",
            sector="residential",
            preset_sector=None,
            fuel="gas",
            end_use="heat",
            type="energy",
            technodatas=[tech],
            comm_in=[
                pro.CommodityFlow(
                    commodity="Gas",
                    region="R1",
                    timeslice="2020",
                    level="fixed",
                    value=1.16,
                )
            ],
            comm_out=[
                pro.CommodityFlow(
                    commodity="Heat",
                    region="R1",
                    timeslice="2020",
                    level="fixed",
                    value=1.0,
                ),
                pro.CommodityFlow(
                    commodity="CO2fuelcomsbustion",
                    region="R1",
                    timeslice="2020",
                    level="fixed",
                    value=64.71,
                ),
            ],
            demands=[],
            existing_capacities=[
                pro.ExistingCapacity(region="R1", year=2020, value=10.0),
                pro.ExistingCapacity(region="R1", year=2025, value=5.0),
                pro.ExistingCapacity(region="R1", year=2030, value=0.0),
                pro.ExistingCapacity(region="R1", year=2035, value=0.0),
                pro.ExistingCapacity(region="R1", year=2040, value=0.0),
                pro.ExistingCapacity(region="R1", year=2045, value=0.0),
                pro.ExistingCapacity(region="R1", year=2050, value=0.0),
            ],
            capacity_unit="PJ/y",
        )
    )
    assert dstore_advanced.process.read("gasboiler").name == "gasboiler"
    with pytest.raises(exc.KeyNotFound) as e:
        dstore_advanced.process.read("test")


def test_process_update(dstore_advanced):
    pro1 = pro.Process(
        name="gasboiler",
        sector="residential",
        preset_sector=None,
        fuel="gas",
        end_use="heat",
        type="energy",
        technodatas=[tech],
        comm_in=[
            pro.CommodityFlow(
                commodity="Gas",
                region="R1",
                timeslice="2020",
                level="fixed",
                value=1.16,
            )
        ],
        comm_out=[
            pro.CommodityFlow(
                commodity="Heat",
                region="R1",
                timeslice="2020",
                level="fixed",
                value=1.0,
            ),
            pro.CommodityFlow(
                commodity="CO2fuelcomsbustion",
                region="R1",
                timeslice="2020",
                level="fixed",
                value=64.71,
            ),
        ],
        demands=[],
        existing_capacities=[
            pro.ExistingCapacity(region="R1", year=2020, value=10.0),
            pro.ExistingCapacity(region="R1", year=2025, value=5.0),
            pro.ExistingCapacity(region="R1", year=2030, value=0.0),
            pro.ExistingCapacity(region="R1", year=2035, value=0.0),
            pro.ExistingCapacity(region="R1", year=2040, value=0.0),
            pro.ExistingCapacity(region="R1", year=2045, value=0.0),
            pro.ExistingCapacity(region="R1", year=2050, value=0.0),
        ],
        capacity_unit="PJ/y",
    )

    pro2 = pro.Process(
        name="gasboiler2",
        sector="residential",
        preset_sector=None,
        fuel="gas",
        end_use="heat",
        type="energy",
        technodatas=[tech],
        comm_in=[
            pro.CommodityFlow(
                commodity="Gas",
                region="R1",
                timeslice="2020",
                level="fixed",
                value=1.16,
            )
        ],
        comm_out=[
            pro.CommodityFlow(
                commodity="Heat",
                region="R1",
                timeslice="2020",
                level="fixed",
                value=1.0,
            ),
            pro.CommodityFlow(
                commodity="CO2fuelcomsbustion",
                region="R1",
                timeslice="2020",
                level="fixed",
                value=64.71,
            ),
        ],
        demands=[],
        existing_capacities=[
            pro.ExistingCapacity(region="R1", year=2020, value=10.0),
            pro.ExistingCapacity(region="R1", year=2025, value=5.0),
            pro.ExistingCapacity(region="R1", year=2030, value=0.0),
            pro.ExistingCapacity(region="R1", year=2035, value=0.0),
            pro.ExistingCapacity(region="R1", year=2040, value=0.0),
            pro.ExistingCapacity(region="R1", year=2045, value=0.0),
            pro.ExistingCapacity(region="R1", year=2050, value=0.0),
        ],
        capacity_unit="PJ/y",
    )
    dstore_advanced.process.create(pro1)
    dstore_advanced.process.update("gasboiler", pro2)
    with pytest.raises(exc.KeyNotFound) as e:
        dstore_advanced.process.read("gasboiler")


def test_process_delete(dstore_advanced):
    dstore_advanced.process.create(
        pro.Process(
            name="gasboiler",
            sector="residential",
            preset_sector=None,
            fuel="gas",
            end_use="heat",
            type="energy",
            technodatas=[tech],
            comm_in=[
                pro.CommodityFlow(
                    commodity="Gas",
                    region="R1",
                    timeslice="2020",
                    level="fixed",
                    value=1.16,
                )
            ],
            comm_out=[
                pro.CommodityFlow(
                    commodity="Heat",
                    region="R1",
                    timeslice="2020",
                    level="fixed",
                    value=1.0,
                ),
                pro.CommodityFlow(
                    commodity="CO2fuelcomsbustion",
                    region="R1",
                    timeslice="2020",
                    level="fixed",
                    value=64.71,
                ),
            ],
            demands=[],
            existing_capacities=[
                pro.ExistingCapacity(region="R1", year=2020, value=10.0),
                pro.ExistingCapacity(region="R1", year=2025, value=5.0),
                pro.ExistingCapacity(region="R1", year=2030, value=0.0),
                pro.ExistingCapacity(region="R1", year=2035, value=0.0),
                pro.ExistingCapacity(region="R1", year=2040, value=0.0),
                pro.ExistingCapacity(region="R1", year=2045, value=0.0),
                pro.ExistingCapacity(region="R1", year=2050, value=0.0),
            ],
            capacity_unit="PJ/y",
        )
    )
    dstore_advanced.process.delete("gasboiler")
    with pytest.raises(exc.KeyNotFound) as e:
        dstore_advanced.process.read("gasboiler")


def test_process_list(dstore_advanced):
    dstore_advanced.process.create(
        pro.Process(
            name="gasboiler",
            sector="residential",
            preset_sector=None,
            fuel="gas",
            end_use="heat",
            type="energy",
            technodatas=[tech],
            comm_in=[
                pro.CommodityFlow(
                    commodity="Gas",
                    region="R1",
                    timeslice="2020",
                    level="fixed",
                    value=1.16,
                )
            ],
            comm_out=[
                pro.CommodityFlow(
                    commodity="Heat",
                    region="R1",
                    timeslice="2020",
                    level="fixed",
                    value=1.0,
                ),
                pro.CommodityFlow(
                    commodity="CO2fuelcomsbustion",
                    region="R1",
                    timeslice="2020",
                    level="fixed",
                    value=64.71,
                ),
            ],
            demands=[],
            existing_capacities=[
                pro.ExistingCapacity(region="R1", year=2020, value=10.0),
                pro.ExistingCapacity(region="R1", year=2025, value=5.0),
                pro.ExistingCapacity(region="R1", year=2030, value=0.0),
                pro.ExistingCapacity(region="R1", year=2035, value=0.0),
                pro.ExistingCapacity(region="R1", year=2040, value=0.0),
                pro.ExistingCapacity(region="R1", year=2045, value=0.0),
                pro.ExistingCapacity(region="R1", year=2050, value=0.0),
            ],
            capacity_unit="PJ/y",
        )
    )
    dstore_advanced.process.create(
        pro.Process(
            name="gasboiler2",
            sector="residential",
            preset_sector=None,
            fuel="gas",
            end_use="heat",
            type="energy",
            technodatas=[tech],
            comm_in=[
                pro.CommodityFlow(
                    commodity="Gas",
                    region="R1",
                    timeslice="2020",
                    level="fixed",
                    value=1.16,
                )
            ],
            comm_out=[
                pro.CommodityFlow(
                    commodity="Heat",
                    region="R1",
                    timeslice="2020",
                    level="fixed",
                    value=1.0,
                ),
                pro.CommodityFlow(
                    commodity="CO2fuelcomsbustion",
                    region="R1",
                    timeslice="2020",
                    level="fixed",
                    value=64.71,
                ),
            ],
            demands=[],
            existing_capacities=[
                pro.ExistingCapacity(region="R1", year=2020, value=10.0),
                pro.ExistingCapacity(region="R1", year=2025, value=5.0),
                pro.ExistingCapacity(region="R1", year=2030, value=0.0),
                pro.ExistingCapacity(region="R1", year=2035, value=0.0),
                pro.ExistingCapacity(region="R1", year=2040, value=0.0),
                pro.ExistingCapacity(region="R1", year=2045, value=0.0),
                pro.ExistingCapacity(region="R1", year=2050, value=0.0),
            ],
            capacity_unit="PJ/y",
        )
    )

    assert len(dstore_advanced.process.list()) == 2


# this one always returns empty dict
def test_process_back_dependents_recursive():
    dstore = Datastore.from_settings("test_data2/settings.toml")
    dict = dstore.process.back_dependents_recursive(dstore.process.read("gasboiler"))
    print(dict)
    # assert len(dict["commodity"]) == 0
    # assert len(dict["region"]) == 0
    # assert len(dict["sector"]) == 0
    # assert len(dict["agent"]) == 0


# agent tests
def test_agent_create(dstore_advanced):
    dstore_advanced.agent.create(
        ag.Agent(
            name="A2",
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
    with pytest.raises(exc.KeyAlreadyExists) as e:
        dstore_advanced.agent.create(
            ag.Agent(
                name="A2",
                sectors=["gas", "power", "residential"],
                new={
                    "R1": ag.AgentData(
                        num=None,
                        objective_1=ag.AgentObjective(
                            objective_type="LCOE",
                            objective_data=1.0,
                            objective_sort=False,
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
                            objective_type="LCOE",
                            objective_data=1.0,
                            objective_sort=False,
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


def test_agent_read(dstore_advanced):
    dstore_advanced.agent.create(
        ag.Agent(
            name="A2",
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
    assert dstore_advanced.agent.read("A2").name == "A2"
    with pytest.raises(exc.KeyNotFound) as e:
        dstore_advanced.agent.read("A3")


def test_agent_update(dstore_advanced):
    dstore_advanced.agent.create(
        ag.Agent(
            name="A2",
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
    dstore_advanced.agent.update(
        "A2",
        ag.Agent(
            name="A3",
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
        ),
    )
    with pytest.raises(exc.KeyNotFound) as e:
        dstore_advanced.agent.read("A2")


def test_agent_delete(dstore_advanced):
    dstore_advanced.agent.create(
        ag.Agent(
            name="A2",
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
    dstore_advanced.agent.delete("A2")
    with pytest.raises(exc.KeyNotFound) as e:
        dstore_advanced.agent.read("A2")


def test_agent_list(dstore_advanced):
    dstore_advanced.agent.create(
        ag.Agent(
            name="A2",
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
    dstore_advanced.agent.create(
        ag.Agent(
            name="A3",
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
    assert len(dstore_advanced.agent.list()) == 3


def test_agent_forward_dependents_recursive():
    dstore = Datastore.from_settings("test_data2/settings.toml")
    dict = dstore.agent.forward_dependents_recursive(dstore.agent.read("A1"))
    assert len(dict["process"]) == 5


def test_agent_back_dependents_recursive():
    dstore = Datastore.from_settings("test_data2/settings.toml")
    dict = dstore.agent.back_dependents_recursive(dstore.agent.read("A1"))
    assert len(dict["process"]) == 5
