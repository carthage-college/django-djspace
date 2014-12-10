#!/bin/bash

cd /d2/django_projects/djspace/static/

mkdir -p files/first-nations-launch-competition/proposal/

mkdir -p files/high-altitude-balloon-payload/cv/
mkdir -p files/high-altitude-balloon-payload/letter-interest/
mkdir -p files/high-altitude-balloon-launch/cv/
mkdir -p files/high-altitude-balloon-launch/letter-interest/

mkdir -p files/higher-education-initiatives/proposal/
mkdir -p files/research-infrastructure/proposal/

mkdir -p files/undergraduate-scholarship/recommendation/
mkdir -p files/undergraduate-scholarship/wsgc-advisor-recommendation/
mkdir -p files/undergraduate-scholarship/signed-certification/
mkdir -p files/undergraduate-scholarship/transcripts/undergraduate
mkdir -p files/undergraduate-scholarship/transcripts/high-school/

mkdir -p files/undergraduate-research/recommendation/
mkdir -p files/undergraduate-research/wsgc-advisor-recommendation/
mkdir -p files/undergraduate-research/signed-certification/
mkdir -p files/undergraduate-research/transcripts/high-school/
mkdir -p files/undergraduate-research/transcripts/undergraduate/

mkdir -p files/graduate-fellowship/proposal/
mkdir -p files/graduate-fellowship/cv/
mkdir -p files/graduate-fellowship/budget/
mkdir -p files/graduate-fellowship/transcripts/undergraduate/
mkdir -p files/graduate-fellowship/transcripts/graduate/
mkdir -p files/graduate-fellowship/recommendation/
mkdir -p files/graduate-fellowship/signed-certification/

mkdir -p files/clark-graduate-fellowship/proposal/
mkdir -p files/clark-graduate-fellowship/cv/
mkdir -p files/clark-graduate-fellowship/budget/
mkdir -p files/clark-graduate-fellowship/transcripts/undergraduate/
mkdir -p files/clark-graduate-fellowship/transcripts/graduate/
mkdir -p files/clark-graduate-fellowship/recommendation/
mkdir -p files/clark-graduate-fellowship/signed-certification/

chown -R www-data:staff files

