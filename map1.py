import folium
import pandas
import pandas as pd

LOC=[1.35943801129225, 103.81768925409193] #SG

col_dict = {
    "RED":"red",
    "GREEN":"darkgreen",
    "BLUE":"blue",
    "PURPLE":"purple",
    "YELLOW":"orange",
    "OTHERS":"darkgray"
}

data = pandas.read_csv("mrtsg.csv")
lat = list(data["Latitude"])
lon = list(data['Longitude'])
mrt = list(data["STN_NAME"])

mrt_line = [col_dict[col] for col in data["COLOR"]]

wiki = ["https://en.wikipedia.org/wiki/" + stn.title().replace(" ", "_").replace("Mrt", "MRT").replace("Lrt", "LRT")
        for stn in data["STN_NAME"]]

new_df = pd.DataFrame(list(zip(mrt, lat, lon, mrt_line, wiki)), columns=['name','lat','lon','color','wiki'])

map = folium.Map(location=LOC, zoom_start=12, tiles="Stamen Terrain")

fg_red = folium.FeatureGroup(name="North-South Line (Red)")
fg_green = folium.FeatureGroup(name="East-West Line (Green)")
fg_blue = folium.FeatureGroup(name="Downtown Line (Blue)")
fg_purple = folium.FeatureGroup(name="North-East Line (Purple)")
fg_yellow = folium.FeatureGroup(name="Circle Line (Yellow)")
fg_gray = folium.FeatureGroup(name="LRT(Gray)")

def fg_def(col_value, fg_name, df):
    new_df_color = df[df['color'] == col_value]
    lat = new_df_color['lat']
    lon = new_df_color['lon']
    mrt = new_df_color['name']
    mrt_line = new_df_color['color']
    wiki = new_df_color['wiki']

    for lt, ln, stat, line_color, wiki_link in zip(lat, lon, mrt, mrt_line, wiki):
        iframe = folium.IFrame(html=f"<h4>{stat}</h4><a href={wiki_link} target='_blank'>Wiki info", width=200, height=100)
        fg_name.add_child(folium.CircleMarker(
            radius=5,
            location=[lt, ln],
            popup=folium.Popup(iframe),
            color=line_color,
            fill=True,
            fill_opacity=0.85,
            ))


fg_dict = {
    "red":fg_red,
    "darkgreen":fg_green,
    "blue":fg_blue,
    "purple":fg_purple,
    "orange":fg_yellow,
    "darkgray":fg_gray,
}

for line_color,fg_name in fg_dict.items():
    fg_def(line_color, fg_name, new_df)

for line_color,fg_name in fg_dict.items():
    map.add_child(fg_name)

map.add_child(folium.LayerControl())
map.save("index.html")

# fg = folium.FeatureGroup(name="SG Map")
#
# for lt, ln, stat, line_color, wiki_link in zip(lat, lon, mrt, mrt_line, wiki):
#     iframe = folium.IFrame(html=f"<h4>{stat}</h4><a href={wiki_link} target='_blank'>Wiki info", width=200, height=100)
#     # fg.add_child(folium.Marker(
#     #     location=[lt, ln],
#     #     popup=folium.Popup(iframe),
#     #     icon=folium.Icon(color=line_color, icon="info-sign")
#     #     ))
#     fg.add_child(folium.CircleMarker(
#         radius=5,
#         location=[lt, ln],
#         popup=folium.Popup(iframe),
#         color=line_color,
#         fill=True,
#         fill_opacity=0.85,
#         ))
#
