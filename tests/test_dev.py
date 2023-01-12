from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pytest
from rasterio import transform

from tests.staging import land_map

TEMP_DIR = Path("temp/")
TEMP_DIR.mkdir(parents=False, exist_ok=True)

"""
# TODO:
FIX
- why the degeneration once borders breached?
ENHANCE
- recalculate the centrality access on each run using contiguity?
- add a fillable geom colour vs. buildable geom
- how to handle ratio of exploration vs. size of green space?
- how to jump roads
- new centralities only along roads?
- add progress bar
- offload from main thread - https://gis.stackexchange.com/a/259707/25383
- whether to try removing initialisation? Doesn't seem feasible - could move to vector as well
- what about moving all state to vector and simply writing to raster?
DO
- two speed - explore and encircle large park areas then fill-in more slowly via neighbours?
OR
- aggressive exploration - only infill neighbours 6 or more? 
- then when a concavity is greater than min - instead of switching straight to buildable - start reverse buffering to allow infill around edges - like deflating a balloon - to preserve shape?
NOTEs
- intentionally tackles a large area to pre-emptively find bottlenecks
- performance remains a significant requirement - using Numba - prototype works (i.e. Numba seems to work from QGIS)
- need to find a way to speed up initialisation - a lot of green access and centrality access to compute
- fairly performant once iterations start
BUGs
- shapely crash for buffer params (resolved by using built-in global vars for buffer params)
- writing vs loading bug (write hadn't completed in time for load... resolved by doing all writes first)
"""


def test_plot(land: land_map.Land):
    """ """
    fig, axes = plt.subplots(3, 2, figsize=(12, 12), squeeze=True, sharex=True, sharey=True)
    fig.suptitle(f"Iteration {land.iters}")
    axes[0][0].imshow(land.state_arr, origin="lower")
    axes[0][0].set_title("land state")
    axes[0][1].imshow(land.green_itx_arr, origin="lower")
    axes[0][1].set_title("green periphery")
    axes[1][0].imshow(land.green_acc_arr, origin="lower")
    axes[1][0].set_title("green access")
    axes[1][1].imshow(land.buildable_arr, origin="lower")
    axes[1][1].set_title("buildable")
    axes[2][0].imshow(land.cent_acc_arr, origin="lower")
    axes[2][0].set_title("cent access")
    axes[2][1].imshow(land.density_arr, origin="lower")
    axes[2][1].set_title("density")
    plt.tight_layout()
    plt.savefig(TEMP_DIR / f"{land.iters}.png", dpi=200)


def test_land_map():
    """ """
    x_span = 6000
    y_span = 4000
    granularity_m = 50
    max_distance_m = 1000
    # y is rows
    extents_arr = np.full((int(y_span / granularity_m), int(x_span / granularity_m)), 0, dtype=np.int_)
    # snip out corner of extents for testing out of bounds
    for x_idx, y_idx in np.ndindex(extents_arr.shape):
        dist = np.hypot(x_idx * granularity_m, y_idx * granularity_m)
        if dist <= 200:
            extents_arr[x_idx, y_idx] = -1
    # snips
    extents_arr[:, 0] = -1
    extents_arr[1, :] = -1
    land = land_map.Land(
        granularity_m=granularity_m,
        max_distance_m=max_distance_m,
        # prepare transform - expects w, s, e, n, cell width, cell height
        extents_transform=transform.from_bounds(0, 0, x_span, y_span, extents_arr.shape[1], extents_arr.shape[0]),
        extents_arr=extents_arr,
        centre_seeds=[(int(x_span / 3), int(y_span / 2))],
        min_green_km2=0.5,
        random_seed=20,
    )
    test_plot(land)
    iters = 500
    for _ in range(iters):
        land.iterate()
        print(land.iters)
        if land.iters < 5 or land.iters % 50 == 0:
            test_plot(land)
    test_plot(land)
    print("here")


def test_recurse_gobble():
    """ """
    test_arr = np.full((100, 100), 0, dtype=np.int_)
    # start in middle
    enough_extents = land_map.continuous_state_extents(test_arr, 50, 50, 0, 200 * 200, 250, 50)
    assert enough_extents
    # start in corner
    enough_extents = land_map.continuous_state_extents(test_arr, 0, 0, 0, 200 * 200, 250, 50)
    assert enough_extents
    # reduce distance - should return False since start node is not included
    enough_extents = land_map.continuous_state_extents(test_arr, 0, 0, 0, 200 * 200, 200, 50)
    assert enough_extents is False


if __name__ == "__main__":
    test_land_map()
    # test_recurse_gobble()
