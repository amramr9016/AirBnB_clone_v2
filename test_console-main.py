#!/usr/bin/python3
import inspect
import io
import sys
import cmd
import shutil

"""
Cleanup file storage
"""
import os
new_file_path = "file.json"
if not os.path.exists(new_file_path):
    try:
        from models.engine.file_storage import FileStorage
        new_file_path = FileStorage._FileStorage__file_path
    except:
        pass
if os.path.exists(new_file_path):
    os.remove(new_file_path)

"""
Backup console file
"""
if os.path.exists("tmp_console_main.py"):
    shutil.copy("tmp_console_main.py", "console.py")
shutil.copy("console.py", "tmp_console_main.py")

"""
Backup models/__init__.py file
"""
if os.path.exists("models/tmp__init__.py"):
    shutil.copy("models/tmp__init__.py", "models/__init__.py")
shutil.copy("models/__init__.py", "models/tmp__init__.py")

"""
Overwrite models/__init__.py file with switch_to_file_storage.py
"""
if os.path.exists("switch_to_file_storage.py"):
    shutil.copy("switch_to_file_storage.py", "models/__init__.py")

"""
Updating console to remove "__main__"
"""
with open("tmp_console_main.py", "r") as new_file_i:
    console_lines = new_file_i.readlines()
    with open("console.py", "w") as new_file_o:
        in_main = False
        for line in console_lines:
            if "__main__" in line:
                in_main = True
            elif in_main:
                if "cmdloop" not in line:
                    new_file_o.write(line.lstrip("    ")) 
            else:
                new_file_o.write(line)

import console

"""
 Create console
"""
new_console_obj = "HBNBCommand"
for name, obj in inspect.getmembers(console):
    if inspect.isclass(obj) and issubclass(obj, cmd.Cmd):
        new_console_obj = obj

new_my_console = new_console_obj(stdout=io.StringIO(), stdin=io.StringIO())
new_my_console.use_rawinput = False

"""
 Exec command
"""
def exec_command(new_my_console, new_the_command, last_lines = 1):
    new_my_console.stdout = io.StringIO()
    real_stdout = sys.stdout
    sys.stdout = new_my_console.stdout
    new_my_console.onecmd(new_the_command)
    sys.stdout = real_stdout
    lines = new_my_console.stdout.getvalue().split("\n")
    return "\n".join(lines[(-1*(last_lines+1)):-1])

"""
 Tests
"""
new_state_name = "California"
new_result = exec_command(new_my_console, "create State name=\"{}\"".format(new_state_name))
if new_result is None or new_result == "":
    print("FAIL: No ID retrieved")

new_state_id = new_result

new_city_name = "San Francisco is super cool"
new_result = exec_command(new_my_console, "create City state_id=\"{}\" name=\"{}\"".format(new_state_id, new_city_name.replace(" ", "_")))
# create City state_id="d363d0fc-509c-4b29-81d0-1ae0b4b7025f" city_name="San_Francisco_is_super_cool"
if new_result is None or new_result == "":
    print("FAIL: No ID retrieved")

new_city_id = new_result

new_user_email = "my@me.com"
new_user_pwd = "pwd"
new_user_fn = "FN"
new_user_ln = "LN"
new_result = exec_command(new_my_console, "create User email=\"{}\" password=\"{}\" frist_name=\"{}\" last_name=\"{}\"".format(new_user_email, new_user_pwd, new_user_fn, new_user_ln))
if new_result is None or new_result == "":
    print("FAIL: No ID retrieved")

new_user_id = new_result

new_place_name = "My house"
new_place_desc = "no description yet"
new_place_nb_rooms = 4
new_place_nb_bath = 0
new_place_max_guests = -3
new_place_price = 100
new_place_lat = -120.12
new_place_lon = 0.41921928
new_result = exec_command(new_my_console, "create Place city_id=\"{}\" user_id=\"{}\" name=\"{}\" description=\"{}\" number_rooms={} number_bathrooms={} max_guest={} price_by_night={} latitude={} longitude={}".format(new_city_id, new_user_id, new_place_name.replace(" ", "_"), new_place_desc.replace(" ", "_"), new_place_nb_rooms, new_place_nb_bath, new_place_max_guests, new_place_price, new_place_lat, new_place_lon))
if new_result is None or new_result == "":
    print("FAIL: No ID retrieved")

new_place_id = new_result

new_result = exec_command(new_my_console, "show Place {}".format(new_place_id))
if new_result is None or new_result == "":
    print("FAIL: empty output")

if "[Place]" not in new_result or new_place_id not in new_result:
    print("FAIL: wrong output format: \"{}\"".format(new_result))

if "city_id" not in new_result or new_city_id not in new_result:
    print("FAIL: missing new information: \"{}\"".format(new_result))

if "user_id" not in new_result or new_user_id not in new_result:
    print("FAIL: missing new information: \"{}\"".format(new_result))

if "name" not in new_result or new_place_name not in new_result:
    print("FAIL: missing new information: \"{}\"".format(new_result))

if "description" not in new_result or new_place_desc not in new_result:
    print("FAIL: missing new information: \"{}\"".format(new_result))

if "number_rooms" not in new_result or str(new_place_nb_rooms) not in new_result:
    print("FAIL: missing new information: \"{}\"".format(new_result))

if "number_bathrooms" not in new_result or str(new_place_nb_bath) not in new_result:
    print("FAIL: missing new information: \"{}\"".format(new_result))

if "max_guest" not in new_result or str(new_place_max_guests) not in new_result:
    print("FAIL: missing new information: \"{}\"".format(new_result))

if "price_by_night" not in new_result or str(new_place_price) not in new_result:
    print("FAIL: missing new information: \"{}\"".format(new_result))

if "latitude" not in new_result or str(new_place_lat) not in new_result:
    print("FAIL: missing new information: \"{}\"".format(new_result))

if "longitude" not in new_result or str(new_place_lon) not in new_result:
    print("FAIL: missing new information: \"{}\"".format(new_result))


print("OK", end="")

shutil.copy("tmp_console_main.py", "console.py")
shutil.copy("models/tmp__init__.py", "models/__init__.py")
