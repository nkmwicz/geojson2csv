# GeoJson2csv

This is a package to convert GeoJSON files to CSV files with a GeoWKT field for the coordinates. It is a simple command line tool without any dependencies. It takes two arguments: the input GeoJSON file and the output CSV file.

## Usage

clone the repository.

```bash
git clone https://github.com/GeoJson2csv/GeoJson2csv.git
```

The command line tool can be run as follows prepending python3 or python to the command depending on the Python version:

```bash
python3 ./geojson2csv.py input.json output.csv
```

You can improve its usability by adding the package's location to your path. In that case, you don't need to prepend python3 or python to the command.

```bash
geojson2csv.py input.json output.csv
```
