"""The init file of the package."""
import dash_leaflet as dl

from .basemaps import basemap_tiles

__version__ = "0.1.0"
__author__ = "Pierrick Rambaud"
__email__ = "pierrick.rambaud49@gmail.com"


class BasemapLayer(dl.TileLayer):
    """A class to represent a basemap layer."""

    def __init__(self, name: str, **kwargs):
        """Initialize the class.

        Args:
            name: The name of the basemap.
            kwargs: any keyword arguments from dash-leaflet TileLayer class knowing that ``url``, ``id`` and ``attribution`` will be ignored.
        """
        # check if the name exists
        if name not in basemap_tiles:
            raise ValueError(
                f"Basemap {name} not found. Available basemaps are: [{', '.join(basemap_tiles.keys())}"
            )

        # get the basemap
        kwargs["url"] = basemap_tiles[name].url
        kwargs["id"] = basemap_tiles[name].id
        kwargs["attribution"] = basemap_tiles[name].attribution
        kwargs["max_zoom"] = kwargs.get("maxZoom", basemap_tiles[name].max_zoom)
        super().__init__(kwargs)
