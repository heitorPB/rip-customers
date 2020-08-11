from app.geo import coordinates


def test_coordinates():
    assert coordinates('São Carlos, SP, BR') == {'latitude': -22.017544,
                                                 'longitude': -47.890971}
    assert coordinates('Aquiraz, CE') == {'latitude': -3.90269,
                                          'longitude': -38.389121}
    assert coordinates('Geneva') == {'latitude': 46.201756,
                                     'longitude': 6.146601}
