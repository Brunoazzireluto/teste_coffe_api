import os
from random import randint
from app import create_app
import random


app = create_app(os.getenv('FLASK_CONFIG') or 'default')

@app.context_processor
def add_imports():
    return dict(random=random)


@app.cli.command()
def test():
    """run the unit test"""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)