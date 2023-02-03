#!/bin/bash

cd /d2/django_projects/djspace/static/

mkdir -p files/applications/clark-graduate-fellowship/
mkdir -p files/applications/first-nations-rocket-competition/
mkdir -p files/applications/graduate-fellowship/
mkdir -p files/applications/high-altitude-balloon-launch/
mkdir -p files/applications/undergraduate-aerospace-design-research-scholarship/
mkdir -p files/applications/higher-education-initiatives/
mkdir -p files/applications/research-infrastructure/
mkdir -p files/applications/undergraduate-research/
mkdir -p files/applications/undergraduate-scholarship/

chown -R www-data:staff files

