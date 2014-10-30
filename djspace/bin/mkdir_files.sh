#!/bin/bash

cd /d2/django_projects/djspace/static/

mkdir files/undergraduate

mkdir files/undergraduate/scholarship/
mkdir files/undergraduate/scholarship/recommendation/
mkdir files/undergraduate/scholarship/signed_certification/
mkdir files/undergraduate/scholarship/transcripts/
mkdir files/undergraduate/scholarship/transcripts/undergraduate
mkdir files/undergraduate/scholarship/transcripts/high_school/
mkdir files/undergraduate/scholarship/wsgc_advisor_recommendation/
mkdir files/undergraduate/research/
mkdir files/undergraduate/research/recommendation/
mkdir files/undergraduate/research/signed_certification/
mkdir files/undergraduate/research/transcripts/
mkdir files/undergraduate/research/transcripts/high_school/
mkdir files/undergraduate/research/transcripts/undergraduate/
mkdir files/undergraduate/research/wsgc_advisor_recommendation/

mkdir files/graduate

sudo chown -R www-data:staff files

