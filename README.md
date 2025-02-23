# bsp-future-urban-growth

This is an evolution of the ideas first explored with the [Future Urban Growth](https://github.com/UCL/BSP-future-urban-growth) project.

This version uses a hybridised road network distance and raster state and depends on [cityseer](https://github.com/benchmark-urbanism/cityseer-api/).

## Concept

1. Preparation:

- Add road network to inputs - this should be a skeleton network - not collector roads
- Decompose network to e.g. 50m
- Compute density access and centres access from each node
- Prepare rasters - including green access and green / urban itx

2. Iters:

- Cell's access to centres is based on nearest node's access + linear distance to that node
- Review itx locations for best ratio of centres / densities (or simply centres?)
- Add new built areas
- Look for areas with highest density / centres ratio along roads (road itx?)
- Add new centres adjacent to roads

## Installation

- `brew install qt5 pyqt pdm qgis`
- `pdm install`
- add `.env` file with path appendages:

```bash
PYTHONPATH="${env:PYTHONPATH}:/Applications/Qgis.app/Contents/Resources/python/plugins:/Applications/Qgis.app/Contents/Resources/python"
```

## Plugin setup

Plugin requires additional pip packages:

> See: [https://enmap-box.readthedocs.io/en/latest/usr_section/usr_installation.html#package-installer]()

```bash
/Applications/QGIS.app/Contents/MacOS/bin/pip install shapely rasterio numba
```

## References

- [http://g-sherman.github.io/plugin_build_tool/](PB Tool)
- [https://qgis.org/pyqgis/3.28/](PyQgis)
- [https://gis-ops.com/qgis-3-plugin-tutorial-plugin-development-reference-guide/](Plugin Guide)
- [https://docs.qgis.org/testing/en/docs/pyqgis_developer_cookbook/index.html](Cookbook)
- [https://webgeodatavore.github.io/pyqgis-samples/index.html](Samples)
- [https://www.geodose.com/2021/03/netcdf-temporal-visualization-qgis.html](temporal range raster)
- [https://anitagraser.com](open source GIS ramblings)
- [https://docs.qgis.org/3.4/en/docs/user_manual/working_with_mesh/mesh_properties.html#what-s-a-mesh](mesh layers)

## Dev

> Using `pb_tool` deploy doesn't seem to copy the files across, so use a softlink instead.

- `pb_tool` uses a `pb_tool.cfg` file.
- Build the resources: `pb_tool compile`.
- Create a softlink from the dev plugin folder to the QGIS plugins directory: `ln -s /Users/gareth/dev/other/BSP-future-urban-growth/futurb /Users/gareth/Library/Application\ Support/QGIS/QGIS3/profiles/default/python/plugins`.
