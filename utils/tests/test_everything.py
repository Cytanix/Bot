# Copyright (c) 2025 SpiritTheWalf and Cytanix
#
# This work is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
# To view a copy of this license, visit https://creativecommons.org/licenses/by-nc-sa/4.0/ or see the LICENSE file.
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
