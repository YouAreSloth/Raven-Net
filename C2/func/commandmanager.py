import importlib
import os
import inspect


def initcommands(cls):
    commands_dir = 'commands'
    for filename in os.listdir(commands_dir):
        if filename.endswith('.py') and filename != '__init__.py':
            module_name = filename[:-3]
            module = importlib.import_module(f'{commands_dir}.{module_name}')
            for name, func in inspect.getmembers(module, inspect.isfunction):
                if name.startswith(f'do_{module_name}'):
                    setattr(cls, name, func)