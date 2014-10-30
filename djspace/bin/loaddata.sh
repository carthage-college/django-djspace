#!/bin/sh

python ../manage.py loaddata ../core/fixtures/*.json --settings=djspace.settings
