#!/usr/bin/python
"""
Module for console
"""
import cmd
import re
import shlex
import ast
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.state import State
from models.city import City



def split_curly_braces(new_e_arg):
    """
    Splits the curly braces for the update method
    """
    new_curly_braces = re.search(r"\{(.*?)\}", new_e_arg)

    if new_curly_braces:
        new_id_with_comma = shlex.split(new_e_arg[:new_curly_braces.span()[0]])
        new_id = [i.strip(",") for i in new_id_with_comma][0]

        new_str_data = new_curly_braces.group(1)
        try:
            new_arg_dict = ast.literal_eval("{" + new_str_data + "}")
        except Exception:
            print("**  invalid dictionary format **")
            return
        return new_id, new_arg_dict
    else:
        new_commands = new_e_arg.split(",")
        if new_commands:
            try:
                new_id = new_commands[0]
            except Exception:
                return "", ""
            try:
                new_attr_name = new_commands[1]
            except Exception:
                return new_id, ""
            try:
                new_attr_value = new_commands[2]
            except Exception:
                return new_id, new_attr_name
            return f"{new_id}", f"{new_attr_name} {new_attr_value}"

class HBNBCommand(cmd.Cmd):
    """
    HBNBCommand console class
    """
    prompt = "(hbnb) "
    valid_classes = ["BaseModel", "User", "Amenity",
                     "Place", "Review", "State", "City"]

    def emptyline(self):
        """
        Do nothing when an empty line is entered.
        """
        pass

    def do_EOF(self, new_arg):
        """
        EOF (Ctrl+D) signal to exit the program.
        """
        return True

    def do_quit(self, new_arg):
        """
        Quit command to exit the program.
        """
        return True
        

    def do_create(self, new_arg):
        """
        Create a new instance of BaseModel and save it to the JSON file.
        Usage: create <class_name>
        """
        try:
            new_class_name = new_arg.split(" ")[0]
            if len(new_class_name) == 0:
                print("** class name missing **")
                return
            if new_class_name and new_class_name not in self.valid_classes:
                print("** class doesn't exist **")
                return

            new_kwargs = {}
            new_commands = new_arg.split(" ")
            for i in range(1, len(new_commands)):
                
                new_key = new_commands[i].split("=")[0]
                new_value = new_commands[i].split("=")[1]
                #new_key, new_value = tuple(new_commands[i].split("="))
                if new_value.startswith('"'):
                    new_value = new_value.strip('"').replace("_", " ")
                else:
                    try:
                        new_value = eval(new_value)
                    except (SyntaxError, NameError):
                        continue
                new_kwargs[new_key] = new_value

            if new_kwargs == {}:
                new_instance = eval(new_class_name)()
            else:
                new_instance = eval(new_class_name)(**new_kwargs)
            storage.new(new_instance)
            print(new_instance.id)
            storage.save()
        except ValueError:
            print(ValueError)
            return

    def do_show(self, new_arg):
        """
        Show the string representation of an instance.
        Usage: show <class_name> <id>
        """
        new_commands = shlex.split(new_arg)

        if len(new_commands) == 0:
            print("** class name missing **")
        elif new_commands[0] not in self.valid_classes:
            print("** class doesn't exist **")
        elif len(new_commands) < 2:
            print("** instance id missing **")
        else:
            new_objects = storage.all()

            new_key = "{}.{}".format(new_commands[0], new_commands[1])
            if new_key in new_objects:
                print(new_objects[new_key])
            else:
                print("** no instance found **")

    def do_destroy(self, new_arg):
        """
        Delete an instance based on the class name and id.
        Usage: destroy <class_name> <id>
        """
        new_commands = shlex.split(new_arg)

        if len(new_commands) == 0:
            print("** class name missing **")
        elif new_commands[0] not in self.valid_classes:
            print("** class doesn't exist **")
        elif len(new_commands) < 2:
            print("** instance id missing **")
        else:
            new_objects = storage.all()
            new_key = "{}.{}".format(new_commands[0], new_commands[1])
            if new_key in new_objects:
                del new_objects[new_key]
                storage.save()
            else:
                print("** no instance found **")

    def do_all(self, new_arg):
        """
        Print the string representation of all instances or a specific class.
        Usage: <User>.all()
                <User>.show()
        """
        new_objects = storage.all()

        new_commands = shlex.split(new_arg)

        if len(new_commands) == 0:
            for key, value in new_objects.items():
                print(str(value))
        elif new_commands[0] not in self.valid_classes:
            print("** class doesn't exist **")
        else:
            for key, value in new_objects.items():
                if key.split('.')[0] == new_commands[0]:
                    print(str(value))
        
    def do_count(self, new_arg):
        """
        Counts and retrieves the number of instances of a class
        usage: <class name>.count()
        """
        new_objects = storage.all()

        new_commands = shlex.split(new_arg)

        if new_arg:
            new_incoming_class_name = new_commands[0]
        count = 0

        if new_commands:
            if new_incoming_class_name in self.valid_classes:
                for obj in new_objects.values():
                    if obj.__class__.__name__ == new_incoming_class_name:
                        count += 1
                print(count)
            else:
                print("** invalid class name **")
        else:
            print("** class name missing **")

    def do_update(self, new_arg):
        """
        Update an instance by adding or updating an attribute.
        Usage: update <class_name> <id> <attribute_name> "<attribute_value>"
        """
        new_commands = shlex.split(new_arg)

        if len(new_commands) == 0:
            print("** class name missing **")
        elif new_commands[0] not in self.valid_classes:
            print("** class doesn't exist **")
        elif len(new_commands) < 2:
            print("** instance id missing **")
        else:
            new_objects = storage.all()

            new_key = "{}.{}".format(new_commands[0], new_commands[1])
            if new_key not in new_objects:
                print("** no instance found **")
            elif len(new_commands) < 3:
                print("** attribute name missing **")
            elif len(new_commands) < 4:
                print("** value missing **")
            else:
                new_obj = new_objects[new_key]
                new_curly_braces = re.search(r"\{(.*?)\}", new_arg)

                if new_curly_braces:
                    # added to catch errors
                    try:
                        new_str_data = new_curly_braces.group(1)

                        new_arg_dict = ast.literal_eval("{" + new_str_data + "}")

                        new_attribute_names = list(new_arg_dict.keys())
                        new_attribute_values = list(new_arg_dict.values())
                        # added to catch exception
                        try:
                            new_attr_name1 = new_attribute_names[0]
                            new_attr_value1 = new_attribute_values[0]
                            setattr(new_obj, new_attr_name1, new_attr_value1)
                        except Exception:
                            pass
                        try:
                            # added to catch exception
                            new_attr_name2 = new_attribute_names[1]
                            new_attr_value2 = new_attribute_values[1]
                            setattr(new_obj, new_attr_name2, new_attr_value2)
                        except Exception:
                            pass
                    except Exception:
                        pass
                else:

                    new_attr_name = new_commands[2]
                    new_attr_value = new_commands[3]

                    try:
                        new_attr_value = eval(new_attr_value)
                    except Exception:
                        pass
                    setattr(new_obj, new_attr_name, new_attr_value)

                new_obj.save()
    
    def default(self, new_arg):
        """
        Default behavior for cmd module when input is invalid
        """
        new_arg_list = new_arg.split('.')

        new_cls_nm = new_arg_list[0]  # incoming class name

        new_command = new_arg_list[1].split('(')

        new_cmd_met = new_command[0]  # incoming command method

        new_e_arg = new_command[1].split(')')[0]  # extra arguments

        new_method_dict = {
                'all': self.do_all,
                'show': self.do_show,
                'destroy': self.do_destroy,
                'update': self.do_update,
                'count': self.do_count
                }

        if new_cmd_met in new_method_dict.keys():
            if new_cmd_met != "update":
                return new_method_dict[new_cmd_met]("{} {}".format(new_cls_nm, new_e_arg))
            else:
                if not new_cls_nm:
                    print("** class name missing **")
                    return
                try:
                    new_obj_id, new_arg_dict = split_curly_braces(new_e_arg)
                except Exception:
                    pass
                try:
                    new_call = new_method_dict[new_cmd_met]
                    return new_call("{} {} {}".format(new_cls_nm, new_obj_id, new_arg_dict))
                except Exception:
                    pass
        else:
            print("*** Unknown syntax: {}".format(new_arg))
            return False
    

if __name__ == '__main__':
    HBNBCommand().cmdloop()
