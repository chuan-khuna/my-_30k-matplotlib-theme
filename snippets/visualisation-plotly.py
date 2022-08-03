import plotly.graph_objects as go
import plotly.express as px
import plotly.io as pio

pio.templates.default = "plotly_dark"

plotly_config = {
    'toImageButtonOptions': {
        'format': 'png',  # one of png, svg, jpeg, webp
        'filename': 'custom_image',
        'height': 900,
        'width': 2100,
        'scale': 1  # Multiply title/legend/axis/canvas sizes by this factor
    }
}

# custom plotly font
_plotly_fontfamily = "Inconsolata"
_plotly_fontsize = 14
pio.templates[pio.templates.default].layout['font']["family"] = _plotly_fontfamily
pio.templates[pio.templates.default].layout['font']["size"] = _plotly_fontsize
pio.templates[pio.templates.default].layout['title']['font']['size'] = round(_plotly_fontsize * 1.6)
