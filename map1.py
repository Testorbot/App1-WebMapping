import folium
import pandas

LOC=[1.35943801129225, 103.81768925409193] #SG

data = pandas.read_csv("mrtsg.csv")
lat = list(data["Latitude"])
lon = list(data['Longitude'])
mrt = list(data["STN_NAME"])
mrt_line = []
wiki = []

for col in data["COLOR"]:
    if col == "RED":
        mrt_line.append("red")
    elif col == "GREEN":
        mrt_line.append("darkgreen")
    elif col == "BLUE":
        mrt_line.append("blue")
    elif col == "PURPLE":
        mrt_line.append("purple")
    elif col == "YELLOW":
        mrt_line.append("orange")
    else:
        mrt_line.append("darkgray")

for stn in data["STN_NAME"]:
    wiki_str = "https://en.wikipedia.org/wiki/" + stn.title().replace(" ", "_").replace("Mrt", "MRT").replace("Lrt", "LRT")
    wiki.append(wiki_str)

map = folium.Map(location=LOC, zoom_start=12, tiles="Stamen Terrain")

fg = folium.FeatureGroup(name="SG Map")

for lt, ln, stat, line_color, wiki_link in zip(lat, lon, mrt, mrt_line, wiki):
    iframe = folium.IFrame(html=f"<h4>{stat}</h4><a href={wiki_link} target='_blank'>Wiki info", width=200, height=100)
    # fg.add_child(folium.Marker(
    #     location=[lt, ln], 
    #     popup=folium.Popup(iframe), 
    #     icon=folium.Icon(color=line_color, icon="info-sign")
    #     ))
    fg.add_child(folium.CircleMarker(
        radius=5,
        location=[lt, ln], 
        popup=folium.Popup(iframe), 
        color=line_color, 
        fill=True,
        fill_opacity=0.85,
        ))

map.add_child(fg)

map.save("index.html")