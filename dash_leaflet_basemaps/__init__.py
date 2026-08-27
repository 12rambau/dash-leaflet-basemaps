"""The init file of the package."""
from urllib.parse import parse_qsl, quote, urlencode, urlparse, urlunparse

import dash_leaflet as dl

from .basemaps import basemap_tiles

__version__ = "0.2.0"
__author__ = "Pierrick Rambaud"
__email__ = "pierrick.rambaud49@gmail.com"


class BasemapLayer(dl.TileLayer):
    """A class to represent a basemap layer."""

    def __init__(
        self, name: str, show_attribution: bool = True, api_key: None | str = None, **kwargs
    ):
        """Initialize the class.

        Args:
            name: The name of the basemap.
            show_attribution: decide if the attribution of the newly added layer should be displayed in leaflet attributions. Must be done in agreement with the licence of each individual layer. Default is ``True``.
            api_key: optional API key appended to the tile URL as a ``key`` query parameter. Existing query parameters and fragments are preserved and the value is percent-encoded.
            kwargs: any keyword arguments from dash-leaflet TileLayer class knowing that ``url``, ``id`` and ``attribution`` will be ignored.
        """
        # check if the name exists
        if name not in basemap_tiles:
            raise ValueError(
                f"Basemap {name} not found. Available basemaps are: [{', '.join(basemap_tiles.keys())}"
            )

        url = basemap_tiles[name].url
        if api_key is not None:
            # append the api_key to the url as a query parameter
            parts = urlparse(url)
            params = parse_qsl(parts.query, keep_blank_values=True)
            params.append(("key", api_key))
            new_query = urlencode(params, quote_via=quote, safe="{}")
            url = urlunparse(parts._replace(query=new_query))

        kwargs["url"] = url
        kwargs["id"] = basemap_tiles[name].id
        kwargs["maxZoom"] = kwargs.get("maxZoom", basemap_tiles[name].max_zoom)

        # add the atribution if requested
        if show_attribution is True:
            kwargs["attribution"] = basemap_tiles[name].attribution

        super().__init__(**kwargs)
