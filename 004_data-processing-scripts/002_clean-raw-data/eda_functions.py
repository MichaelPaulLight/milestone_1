import plotly.express as px
import json
import requests

def choropleth(data, hue_column, slider_column=None, title=None):
    """
    Create a choropleth map of California counties, with an optional slider.
    
    Parameters:
    data (pandas.DataFrame): Dataframe containing the data. Must have 'county_name' column.
    hue_column (str): Name of the column to be visualized as colors.
    slider_column (str, optional): Name of the column to be used for the slider animation. If None, a static map is created.
    title (str, optional): Title for the map. If None, a default title is used.
    
    Returns:
    plotly.graph_objects.Figure: A Plotly figure object containing the choropleth map.
    """
    # Load GeoJSON data for California counties
    url = "https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json"
    counties = json.loads(requests.get(url).text)
    
    # Filter for only California counties (FIPS codes starting with '06')
    california_counties = {
        "type": "FeatureCollection",
        "features": [feature for feature in counties["features"] if feature["properties"]["STATE"] == "06"]
    }
    
    # Create a mapping of county names to FIPS codes
    county_to_fips = {feature["properties"]["NAME"]: feature["id"] for feature in california_counties["features"]}
    
    # Add FIPS codes to the dataframe
    data['fips'] = data['county_name'].map(county_to_fips)
    
    # Filter the geojson to include only counties present in the data
    california_counties['features'] = [
        feature for feature in california_counties['features']
        if feature['id'] in data['fips'].values
    ]
    
    # Prepare the base arguments for px.choropleth_mapbox
    choropleth_args = {
        "data_frame": data,
        "geojson": california_counties,
        "locations": 'fips',
        "color": hue_column,
        "hover_name": 'county_name',
        "hover_data": [hue_column],
        "title": title or f'{hue_column} by County in California',
        "mapbox_style": "carto-positron",
        "center": {"lat": 37.0, "lon": -120.0},
        "zoom": 5,
        "opacity": 0.7,
        "color_continuous_scale": "Magma",
        "range_color": [data[hue_column].min(), data[hue_column].max()],
        "labels": {hue_column: hue_column.replace('_', ' ').title()},
        "width": 900,
        "height": 600
    }
    
    # Add animation_frame if slider_column is provided
    if slider_column:
        choropleth_args["animation_frame"] = slider_column
        choropleth_args["labels"][slider_column] = slider_column.replace('_', ' ').title()
        choropleth_args["title"] += f' (Animated by {slider_column})'
    
    # Create the choropleth map
    fig = px.choropleth_mapbox(**choropleth_args)

    # Update layout to remove unnecessary elements and add county outlines
    fig.update_layout(
        margin={"r":0,"t":30,"l":0,"b":0},
        mapbox=dict(
            layers=[
                dict(
                    sourcetype='geojson',
                    source=california_counties,
                    type='line',
                    line=dict(width=1),
                    color='white',
                    below='traces'
                )
            ]
        )
    )

    return fig