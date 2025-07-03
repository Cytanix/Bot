"""Runs every test"""
import subprocess
import sys
import os

python_files = [
    'test_connection.py',
    'test_levels.py',
    'test_logs.py',
    'test_punishments.py',
    'test_registration.py',
    'test_regroles.py',
    'test_cc.py',
    'test_redis.py',
    'test_registration.py'
]

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

for file in python_files:
    print(f"Running {file}")
    subprocess.run(['.venv/bin/python', '-m', 'utils.' + file.replace("\\", ".").replace(".py", "")],
                   stdout=sys.stdout,
                   stderr=sys.stderr,
                   env={**os.environ, 'PYTHONPATH': project_root},
                   check=True)
