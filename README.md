# SAFE
Stratified Assessment of Forecasts over Earth

### Installation

`pip install safe-earth`

To build from source: `git clone git@github.com:N-Masi/safe.git`

### Example

An example of using the package to collect metrics on 6 AIWP models across the territory, subregion, and income 
attributes is availabe in `demos/wb2_240x121.py`. It assesses the models using 2020 ERA5 data.

### Data Notes

To unify the coordinate system across all integrated data sources, latitude ranges [-90, 90] with index 0 at -90, and longitude [-180, 180) but with index 0 at 0 and a wraparound from 180 to -180 in the middle. This is because metadata sourced from pygeoboundaries_geolab follows this coordinate system, and it is easiest to bring tabular data into conformance.

### Testing

Run `pytest` in the of the source repository directory.
