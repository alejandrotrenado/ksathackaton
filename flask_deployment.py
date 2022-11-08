from flask import Flask
from flask import request
from flask import render_template
import pandas as pd
import folium
from folium.plugins import HeatMap
from app.interfaces import cds_downloader 
from libraries.folium_jsbutton import JsButton

app = Flask(__name__)
start_date = "2021-01-05"
end_date = "2021-01-05"



def download_data(start_date:str, end_date:str, square:list) -> pd.DataFrame :
    """Function to download the data from the API and transform it to pandas Dataframe
    
    params
    start_date: start date to download data
    end_date: end date to download data
    
    output
    data: pandas dataframe containing the ammonia by date"""

    downloader = cds_downloader.CDS_downloader(['ammonia'],
                                                start_date,end_date,square)

    # WARNING: THIS CALLS ARE MADE BECAUSE LACK OF TIME run_request download de data from the api, debug download doesnt download anything (read the previous .nc file downloaded)
    # chusta_debug reads the csv imported from the interpolation

    # data = downloader.run_request()
    # data = downloader.chusta_debug()
    data = downloader.debug_download()
    
    #WARNING esto está en formato de str, no datetime
    data["time"]= data["time"].map(lambda x: str(x)[-8:])
    return data



def create_html(start_date:str,end_date:str,square:list):
    """Function that creates the heatmap and map and save it in an html file
    params
    start_date: start date to download data
    end_date: end date to download data
    
    output
    data: pandas dataframe containing the ammonia by date"""

    #Download data from API
    global data_concentration
    data_concentration = download_data(start_date,end_date, square)
    #WARNING el tiempo no iria asi, es con la estructura que venga por parametro de las cajas
    data_concentration = data_concentration[data_concentration["time"]=="00:00:00"]
    convert_dict = {"latitude":float,"longitude":float,"nh3_conc":float}
    data_concentration = data_concentration.astype(convert_dict)

    #create map and heatmap and add it as child
    hmap = folium.Map(location=[42.6, 0.65],zoom_start=8)
    max_amount = data_concentration["nh3_conc"].max()
    hm_wide = HeatMap(list(zip(data_concentration["latitude"].values,
                                data_concentration["longitude"].values,
                                data_concentration["nh3_conc"].values)),radius=17,
                        blur=20,max_zoom=1)
    hmap.add_child(hm_wide)

    #Add form and legend to the html with the new class 
    formulario = JsButton(title="""<fieldset style="width:400px"><legend><font face="arial">Data</font>:</legend><div style="text-align: center;"><img src="farmsat.png" width="130" height="100"><br><br></div><label for="fname"><font face="arial">Latitude</font></label><input type="text" id="lat" name="fname" value="41.7911" position="center"><br><br><label for="lname"><font face="arial">Length</font></label><input type="text" id="length" name="lname" value="0.8109"><br><br><label for="dog-names"><font face="arial">Technique</font></label><select name="dog-names" id="dog-names"><option value="select"><font face="arial">Purin</font></option><option value="fosogest">Enrejillado y foso gestacion</option><option value="camapaja">Cama de paja</option><option value="aireventilacion">Aire y ventilación</option><option value="fosorampa">Foso en rampa</option><option value="fosopendiente">Enrejillado foso pendiente</option><option value="fosocebo">Enrejillado y foso cebo</option><option value="fosov">Enrejillado y foso v</option><option value="retgallinaza">Retirada gallinaza</option><option value="secgallinaza">Secado gallinaza</option><option value="bebederos">Bebederos</option><option value="vacgest">Vaciado gestacion</option><option value="vactrans">Vaciado transicion</option><option value="vaccebo">Vaciado cebo</option><option value="dietatrans">Dieta transicion</option><option value="piensos">Piensos</option><option value="acidifpienso">Acidificantes pienso</option><option value="dietacebo">Dieta cebo</option><option value="micropienso">Microorganismos pienso</option><option value="microfoso">Microorganismos foso</option><option value="pajapic">Paja picada</option><option value="lanaflot">Lana flotante</option><option value="costranat">Costra natural</option><option value="bandasmang">Bandas mangueras</option><option value="bandasdisc">Bandas discos</option><option value="inyeccion">Inyeccion</option><option value="entpurin">Enterrado purin</option><option value="entest">Enterrado estiercol</option></select></select><br><br><label for="m2"><font face="arial">m2</font></label><input type="text" id="m2" name="m2" value="1500"><br><br><div><input type="radio" id="NH3" name="gas" checked=true value="NH3"<label for="NH3"><font face="arial"> NH3</font></label></div><div><input type="radio" id="CH4" name="gas" value="CH4"><label for="CH4"><font face="arial">CH4</font></label></div><br><input type="submit" value="Update"></fieldset>""")
    hmap.add_child(formulario).add_to(hmap)

    legend = JsButton(title="""<img src="legend_bueno.png" width=400>"""
    ).add_to(hmap)
    hmap.add_child(legend)
    hmap.save("templates/heatmap.html")

    return

@app.route("/updateMap",methods = ['POST'])
def update_map():
    print(request.args.get('formulario'))
    return render_template("heatmap.html")
    

@app.route("/drawMap")
def draw_map():
    create_html(start_date, end_date, [42.84, -0.23, 40.91,3.09])
    return render_template("heatmap.html")

if __name__ == '__main__':
    # run app in debug mode on port 5000
    app.run(debug=True, port=5000)