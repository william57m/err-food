# ErrFood

[![Build Status](https://travis-ci.org/william57m/err-food.svg?branch=master)](https://travis-ci.org/william57m/err-food)

## Overview

This plugin is a eating food reminder and a random restaurant picker (from raw list or yelp)

## Configuration

```
!plugin config Food { 'API_KEY': 'TO_BE_DEFINED', 'LATITUDE': '45.503215', 'LONGITUDE': '-73.571466', 'RADIUS_METERS': '1000'}
```

## Usage

Choose a random restaurant from a raw list: `!resto pick`

Choose a random restaurant from yelp around your position: `!resto yelp`

## Run tests

```
tox
```
