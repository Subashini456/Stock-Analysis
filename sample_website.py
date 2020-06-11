from flask import Flask,render_template

#instantiating 
app = Flask(__name__)


#plot fun mapped '/plot' hence triggers plot() to execute
@app.route('/plot/')
def plot(): 
    from pandas_datareader import data
    import datetime
    from bokeh.plotting import figure,show,output_file
    from bokeh.embed import components
    from bokeh.resources import CDN #CDN = Content Delivery Network

    start = datetime.datetime(2019,11,2)
    end = datetime.datetime(2020,3,10)

    df = data.DataReader(name="GOOG",data_source="yahoo",start=start,end = end)

    #indermediate data to avoid bohek confusion
    def inc_dec(c,o):
        if c>o:
            value ="Increase"
        elif c<o:
            value ="Decrease"
        else:
            value = "Equal"
        return value    

    #creating new column
    df["Status"] = [inc_dec(c,o) for c,o in zip(df.Close,df.Open)]
    df["Middle"] = (df.Open+df.Close)/2
    df["Height"] = abs(df.Open-df.Close)

    #sizing_mode="scale_width" resizes the chart based on window size
    p = figure(x_axis_type="datetime",width=1000,height=300,sizing_mode="scale_width") 
    p.title.text="Candlestick Chart"
    p.grid.grid_line_alpha = 0.3 #alpha denotes the level of transperancy og the grid horizontal lines

    hours_12=12*60*60*1000

    p.segment(df.index,df.High,df.index,df.Low,color="black")

    p.rect(df.index[df.Status == "Increase"],df.Middle[df.Status == "Increase"],hours_12,
        df.Height[df.Status == "Increase"],fill_color="#CCFFFF",line_color="black")

    p.rect(df.index[df.Status == "Decrease"],df.Middle[df.Status == "Decrease"],hours_12,
        df.Height[df.Status == "Decrease"],fill_color="#FF3333",line_color="black")

    script1,div1 = components(p)
    cdn_js = CDN.js_files[0]
    return render_template("plot.html",script1 = script1,div1 = div1,cdn_js = cdn_js)



@app.route('/')
def home():
    #render template - access html files stored in python application & display the html on requested url
    return render_template("home.html")

@app.route('/about/')
def about():
    return render_template("about.html")

if __name__== "__main__":
    app.run(debug = True)
