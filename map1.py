import folium
import pandas

#Importing the volcano text file with all the coordinates in it 
data = pandas.read_csv("Section17/Volcanoes.txt")

#Importing the lat, long coordinates into a list from the Volcano txt file
lat = list(data["LAT"])
lon = list(data["LON"])

#Importing the elevation data into a list:
elev = list(data["ELEV"])

#Function for giving a color based on elevation
def color_producer(elevation):
    if elevation < 1000:
        return 'green'
    elif 1000 <= elevation < 3000:
        return 'orange'
    else:
        return 'red'


#Creating the map Object
map = folium.Map(location = [38.58, -99.09], zoom_start = 6, tiles = "Stamen Terrain") #Alternative tile: Mapbox Bright

#Feature group so you can store all of these objects in it, to make everything more organized
#Feature group for volcanoes
fgv = folium.FeatureGroup(name = "Volcanoes")

#Creating the map Marker (A single map Marker)
#fg.add_child(folium.Marker(location = [38.2, -99.1], popup = "Hi I'm a Markiplier!", icon = folium.Icon(color = 'green')))

#Using a for loop to create multiple markers
"""for coordinates in [[38.2, -99.1],[39.2, -97.1]]:
    fg.add_child(folium.Marker(location = coordinates, popup = "Hi I'm a Markiplier!", icon = folium.Icon(color = 'green')))"""

#The zip function basically allows you to iterate through different things at the same time -
#for i, j in zip([1,2,3], [4,5,6]):
"""for i, j in zip([1,2,3], [4,5,6]):
        print(i, "and", j)"""
#Would print
"""1 and 4
   2 and 5
   3 and 6"""
for lt,ln, el in zip(lat,lon, elev):
    fgv.add_child(folium.CircleMarker(location = [lt,ln], radius = 6, popup = str(el)+ " m",
    fill_color = color_producer(el), color = 'grey', fill_opacity = 0.7))
    #Original Marker:
    #fg.add_child(folium.Marker(location = [lt,ln], popup = str(el) + " m", icon = folium.Icon(color = color_producer(el))))

#Feature group for Population
fgp = folium.FeatureGroup(name = "Population")


#Geo Json (world.json contains geolocational data):
    #Geolocational data consists of using polygons to shape out areas
    #r denotes opening in read mode
    #This should set the fill color of a polygon to yellow if the population is less than 10 million, orange if higher, and then red if higher than that
    #POP2005 is the population 
fgp.add_child(folium.GeoJson(data = open ('Section17/world.json', 'r', encoding='utf-8-sig').read(), 
style_function= lambda x: {'fillColor': 'green' if x['properties']['POP2005'] < 10000000 
else 'orange' if 10000000 <= x ['properties'] ['POP2005'] < 20000000 else 'red'}))

#Adding the feature groups into the map
map.add_child(fgv)
map.add_child(fgp)

#Adding a control panel to turn layers on/off (In this case you're adding a child object to the map itself):
#Note that you must do this after the the fg gets added to the map. The feature group builds all the layers and polygons first
map.add_child(folium.LayerControl())

#Saving it into a html file so that it can process this 
map.save("Section17/Map1.html")
