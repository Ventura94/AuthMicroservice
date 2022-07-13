from tests.auth_fixtutes import *

def test_clean_data(user_update_form_class, user_dict_not_password):
    result = user_update_form_class.clean_data(**user_dict_not_password)
    assert result == {'user_id': 'jonhdoe12', 'username': 'johndoe', 'role': ['default']}

