#!/bin/bash
python3 -m qbar.main --config=qbar-default.yml&
python3 -m qbar.main --config=bottom.yml --bottom=True
