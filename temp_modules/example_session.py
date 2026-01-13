import modules.session as session
import keys
import temp_modules.test_characters as test_characters
import json
import modules.prompt_builder as prompt_builder


session_instance = session.Session(api_key=keys.api_key, world=test_characters.test_world)

session_instance.add_location(test_characters.test_location, session_instance.client)


session_instance.add_character(test_characters.test_char)
session_instance.add_character(test_characters.test_char2)
session_instance.add_player(test_characters.test_player)

full_character_list = [test_characters.test_char, test_characters.test_char2]

loc_name = test_characters.test_location.name
session_instance.locations[loc_name].add_character(test_characters.test_char, (0,0))
session_instance.locations[loc_name].add_character(test_characters.test_char2, (1,1))
session_instance.locations[loc_name].add_player_character(test_characters.test_player, (2,2))

