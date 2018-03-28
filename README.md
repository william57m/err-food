# ErrFood

[![Build Status](https://travis-ci.org/william57m/err-food.svg?branch=master)](https://travis-ci.org/william57m/err-food)

## Overview

This plugin is a eating food reminder and a random restaurant picker

## Configuration

Trigger food_time_call function at 11:30 and return the result in the channel @mix-squad

```
!plugin config Food { 'API_KEY': 'TO_BE_DEFINED', 'LATITUDE': '45.503215', 'LONGITUDE': '-73.571466', 'RADIUS_METERS': '1000'}
```

## Usage

Choose a restaurant: `!food-pick`

## Run tests
```
pip install -r requirements.txt
pip install -r dev-requirements.txt
pytest tests.py
```