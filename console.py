#!/usr/bin/python3
"""Command line interface for interacting with AirBnB database."""
import cmd
from models import storage
from models.base_model import BaseModel


class HBNBCommand(cmd.Cmd):
    """Command line interpreter for AirBnB."""

    prompt = "(hbnb) "

    def emptyline(self):
        """Do nothing on empty line."""
        pass

    def do_quit(self, arg):
        """Quit command to exit the program."""
        return True

    def do_EOF(self, arg):
        """Handles EOF."""
        print()
        return True

    def do_create(self, arg):
        """Create a new instance of a model."""
        if not arg:
            print("** class name missing **")
            return
        try:
            new_instance = eval(arg)()
            new_instance.save()
            print(new_instance.id)
        except NameError:
            print("** class doesn't exist **")

    def do_show(self, arg):
        """Prints the string representation of an instance."""
        args = arg.split()
        if not arg:
            print("** class name missing **")
            return
        try:
            class_name = args[0]
            obj_id = args[1]
            objs = storage.all()
            key = "{}.{}".format(class_name, obj_id)
            print(objs[key])
        except IndexError:
            print("** instance id missing **")
        except KeyError:
            print("** no instance found **")
        except NameError:
            print("** class doesn't exist **")

    def do_destroy(self, arg):
        """Deletes an instance based on the class name and id."""
        args = arg.split()
        if not arg:
            print("** class name missing **")
            return
        try:
            class_name = args[0]
            obj_id = args[1]
            objs = storage.all()
            key = "{}.{}".format(class_name, obj_id)
            del objs[key]
            storage.save()
        except IndexError:
            print("** instance id missing **")
        except KeyError:
            print("** no instance found **")
        except NameError:
            print("** class doesn't exist **")

    def do_all(self, arg):
        """Prints all string representation of all instances."""
        if not arg:
            objs = storage.all()
            print([str(obj) for obj in objs.values()])
        else:
            try:
                objs = storage.all(eval(arg))
                print([str(obj) for obj in objs.values()])
            except NameError:
                print("** class doesn't exist **")

    def do_update(self, arg):
        """Updates an instance based on the class name and id."""
        args = arg.split()
        if not arg:
            print("** class name missing **")
            return
        try:
            class_name = args[0]
            obj_id = args[1]
            objs = storage.all()
            key = "{}.{}".format(class_name, obj_id)
            obj = objs[key]
            if len(args) < 3:
                print("** attribute name missing **")
                return
            if len(args) < 4:
                print("** value missing **")
                return
            setattr(obj, args[2], args[3])
            obj.save()
        except IndexError:
            print("** instance id missing **")
        except KeyError:
            print("** no instance found **")
        except NameError:
            print("** class doesn't exist **")


if __name__ == "__main__":
    HBNBCommand().cmdloop()
