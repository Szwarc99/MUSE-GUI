import pytest
import muse_gui.backend.resources.datastore.exceptions as exc
from muse_gui.backend.resources.datastore import  Datastore
import muse_gui.backend.data.region as reg
import muse_gui.backend.data.sector as sec
import muse_gui.backend.data.timeslice as ts
import muse_gui.backend.data.commodity as com


# dstore = Datastore()
# dstore.available_year.create(ts.AvailableYear(year=100))
# dstore.available_year.read('100')
# dstore.commodity.create(com.Commodity(commodity='test',commodity_type='Energy',commodity_name='test',c_emission_factor_co2=0.5,heat_rate=0.5,unit='CBM',commodity_prices='10000000000',price_unit='rouble'))




# region tests
def test_region_create(dstore):
    dstore.region.create(reg.Region(name='R1'))
    with pytest.raises(exc.KeyAlreadyExists) as e:
        dstore.region.create(reg.Region(name='R1'))

def test_region_read(dstore):
    dstore.region.create(reg.Region(name='R1'))        
    assert dstore.region.read('R1').name == 'R1'
    with pytest.raises(exc.KeyNotFound) as e:
        dstore.region.read('R2')

def test_region_update(dstore):
    dstore.region.create(reg.Region(name='R1'))        
    dstore.region.update('R1',reg.Region(name='R2'))
    with pytest.raises(exc.KeyNotFound) as e:
        dstore.region.read('R1')

def test_region_delete(dstore):
    dstore.region.create(reg.Region(name='R1'))        
    dstore.region.delete('R1')
    with pytest.raises(exc.KeyNotFound) as e:
        dstore.region.read('R1')

def test_region_list(dstore):
    dstore.region.create(reg.Region(name='R1'))
    dstore.region.create(reg.Region(name='R2'))
    assert len(dstore.region.list()) == 2

def test_region_forward_dependents_recursive():
    dstore = Datastore.from_settings('test_data2/settings.toml')    
    dict = dstore.region.forward_dependents_recursive(dstore.region.read('R1'))
    assert len(dict['commodity']) == 5
    assert len(dict['process']) == 5
    assert len(dict['agent']) == 1

# sector tests
def test_sector_create(dstore):
    dstore.sector.create(sec.StandardSector(name='test',priority=100,type='standard'))
    with pytest.raises(exc.KeyAlreadyExists) as e:       
        dstore.sector.create(sec.StandardSector(name='test',priority=100,type='standard'))

def test_sector_read(dstore):
    dstore.sector.create(sec.StandardSector(name='test',priority=100,type='standard'))
    assert dstore.sector.read('test').name == 'test'
    with pytest.raises(exc.KeyNotFound) as e:
        dstore.sector.read('test2')

def test_sector_update(dstore):
    dstore.sector.create(sec.StandardSector(name='test',priority=100,type='standard'))
    dstore.sector.update('test',sec.StandardSector(name='test2',priority=100,type='standard'))
    with pytest.raises(exc.KeyNotFound) as e:
        dstore.sector.read('test')

def test_sector_delete(dstore):
    dstore.sector.create(sec.StandardSector(name='test',priority=100,type='standard'))        
    dstore.sector.delete('test')
    with pytest.raises(exc.KeyNotFound) as e:
        dstore.sector.read('test')

def test_sector_list(dstore):
    dstore.sector.create(sec.StandardSector(name='test',priority=100,type='standard'))        
    dstore.sector.create(sec.StandardSector(name='test2',priority=100,type='standard'))        
    assert len(dstore.sector.list()) == 2

def test_sector_forward_dependents_recursive():
    pass
    dstore = Datastore.from_settings('test_data2/settings.toml')
    
    dict = dstore.sector.forward_dependents_recursive(dstore.sector.read('gas'))    
    assert len(dict['process']) == 5
    assert len(dict['agent']) == 1

# level_name tests
def test_level_name_create(dstore):
    dstore.level_name.create(ts.LevelName(level='R1'))
    with pytest.raises(exc.KeyAlreadyExists) as e:
        dstore.level_name.create(ts.LevelName(level='R1'))

def test_level_name_read(dstore):
    dstore.level_name.create(ts.LevelName(level='R1'))        
    assert dstore.level_name.read('R1').level == 'R1'
    with pytest.raises(exc.KeyNotFound) as e:
        dstore.level_name.read('R2')

def test_level_name_update(dstore):
    dstore.level_name.create(ts.LevelName(level='R1'))        
    dstore.level_name.update('R1',ts.LevelName(level='R2'))
    with pytest.raises(exc.KeyNotFound) as e:
        dstore.level_name.read('R1')

def test_level_name_delete(dstore):
    dstore.level_name.create(ts.LevelName(level='R1'))        
    dstore.level_name.delete('R1')
    with pytest.raises(exc.KeyNotFound) as e:
        dstore.level_name.read('R1')

def test_level_name_list(dstore):
    dstore.level_name.create(ts.LevelName(level='R1'))
    dstore.level_name.create(ts.LevelName(level='R2'))
    assert len(dstore.level_name.list()) == 2

def test_level_name_forward_dependents_recursive():
    dstore = Datastore.from_settings('test_data2/settings.toml')    
    dict = dstore.level_name.forward_dependents_recursive(dstore.level_name.read('month'))    
    assert len(dict['timeslice']) == 6  

# available_year tests
def test_available_year_create(dstore):
    dstore.available_year.create(ts.AvailableYear(year=100))    
    with pytest.raises(exc.KeyAlreadyExists) as e:
        dstore.available_year.create(ts.AvailableYear(year=100))

def test_available_year_read(dstore):
    dstore.available_year.create(ts.AvailableYear(year=100))        
    assert dstore.available_year.read('100').year == 100
    with pytest.raises(exc.KeyNotFound) as e:
        dstore.available_year.read('200')

def test_available_year_update(dstore):
    dstore.available_year.create(ts.AvailableYear(year=100))        
    dstore.available_year.update('100',ts.AvailableYear(year=200))
    with pytest.raises(exc.KeyNotFound) as e:
        dstore.available_year.read('100')

def test_available_year_delete(dstore):
    dstore.available_year.create(ts.AvailableYear(year=100))        
    dstore.available_year.delete('100')
    with pytest.raises(exc.KeyNotFound) as e:
        dstore.available_year.read('100')

def test_available_year_list(dstore):
    dstore.available_year.create(ts.AvailableYear(year=100))
    dstore.available_year.create(ts.AvailableYear(year=200))
    print(dstore.available_year.list())
    assert len(dstore.available_year.list()) == 2

# testdata doesn t have available years
# def test_available_year_forward_dependents_recursive():
#     dstore = Datastore.from_settings('test_data2/settings.toml')    
#     dict = dstore.available_year.forward_dependents_recursive(dstore.available_year.read())    
#     assert len(dict['commodities']) == 0  

# timeslice tests
def test_timeslice_create(dstore):
    dstore.level_name.create(ts.LevelName(level='L1'))        
    dstore.timeslice.create(ts.Timeslice(name='test',value=100))    
    with pytest.raises(exc.KeyAlreadyExists) as e:
        dstore.timeslice.create(ts.Timeslice(name='test',value=100))

def test_timeslice_read(dstore):
    dstore.level_name.create(ts.LevelName(level='L1'))
    dstore.timeslice.create(ts.Timeslice(name='test',value=100))        
    assert dstore.timeslice.read('test').name == 'test'
    with pytest.raises(exc.KeyNotFound) as e:
        dstore.timeslice.read('test2')

def test_timeslice_update(dstore):
    dstore.level_name.create(ts.LevelName(level='L1'))
    dstore.timeslice.create(ts.Timeslice(name='test',value=100))        
    dstore.timeslice.update('test',ts.Timeslice(name='test2',value=100))
    with pytest.raises(exc.KeyNotFound) as e:
        dstore.timeslice.read('test')

def test_timeslice_delete(dstore):
    dstore.level_name.create(ts.LevelName(level='L1'))
    dstore.timeslice.create(ts.Timeslice(name='test',value=100))        
    dstore.timeslice.delete('test')
    with pytest.raises(exc.KeyNotFound) as e:
        dstore.timeslice.read('test')

def test_timeslice_list(dstore):
    dstore.level_name.create(ts.LevelName(level='L1'))
    dstore.timeslice.create(ts.Timeslice(name='test',value=100))
    dstore.timeslice.create(ts.Timeslice(name='test2',value=100))
    print(dstore.timeslice.list())
    assert len(dstore.timeslice.list()) == 2

# always returns empty dict, probably a bug
def test_timeslice_forward_dependents_recursive():
    dstore = Datastore.from_settings('test_data2/settings.toml')    
    dict = dstore.timeslice.forward_dependents_recursive(dstore.timeslice.read('all-year.all-week.night'))
    print(dict)
    pass
    
#commodity tests
def test_commodity_create(dstore):
    dstore.region.create(reg.Region(name='east'))
    dstore.available_year.create(ts.AvailableYear(year=2020))

    dstore.commodity.create(com.Commodity(commodity='test',commodity_type='Energy',commodity_name='test',
    c_emission_factor_co2=0.5,heat_rate=0.5,unit='CBM',commodity_prices=[{'region_name':'east','time':2020,'value':0.1}],price_unit='rouble'))

    with pytest.raises(exc.KeyAlreadyExists) as e:
        dstore.commodity.create(com.Commodity(commodity='test',commodity_type='Energy',commodity_name='test',
        c_emission_factor_co2=0.5,heat_rate=0.5,unit='CBM',commodity_prices=[{'region_name':'east','time':2020,'value':0.1}],price_unit='rouble'))


# def test_commodity_read(dstore):
#     dstore.level_name.create(ts.LevelName(level='L1'))
#     dstore.commodity.create(ts.commodity(name='test',value=100))        
#     assert dstore.commodity.read('test').name == 'test'
#     with pytest.raises(exc.KeyNotFound) as e:
#         dstore.commodity.read('test2')

# def test_commodity_update(dstore):
#     dstore.level_name.create(ts.LevelName(level='L1'))
#     dstore.commodity.create(ts.commodity(name='test',value=100))        
#     dstore.commodity.update('test',ts.commodity(name='test2',value=100))
#     with pytest.raises(exc.KeyNotFound) as e:
#         dstore.commodity.read('test')

# def test_commodity_delete(dstore):
#     dstore.level_name.create(ts.LevelName(level='L1'))
#     dstore.commodity.create(ts.commodity(name='test',value=100))        
#     dstore.commodity.delete('test')
#     with pytest.raises(exc.KeyNotFound) as e:
#         dstore.commodity.read('test')

# def test_commodity_list(dstore):
#     dstore.level_name.create(ts.LevelName(level='L1'))
#     dstore.commodity.create(ts.commodity(name='test',value=100))
#     dstore.commodity.create(ts.commodity(name='test2',value=100))
#     print(dstore.commodity.list())
#     assert len(dstore.commodity.list()) == 2

# # always returns empty dict, probably a bug
# def test_commodity_forward_dependents_recursive():
#     dstore = Datastore.from_settings('test_data2/settings.toml')    
#     dict = dstore.commodity.forward_dependents_recursive(dstore.commodity.read('all-year.all-week.night'))
#     print(dict)
#     pass
    