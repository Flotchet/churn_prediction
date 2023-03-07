
One can attempt to deploy this code by following the instructions found on the official website:
[Matplotlib Website](https://matplotlib.org/stable/gallery/user_interfaces/web_application_server_sgskip.html)
Place, add this style in 'your_file.html'.
One can adjust the image size in the html file. The data/variable passed to the page is user_data.

<head>
<style>
    .image600{
        width:100%;
        max-width:600px;
        height:100%;
        max-height:200px;
    }
</style>  
</head>
<p>
    <img class = 'image600' src='data:image/png;base64,{{ user_image }}'/>"   
</p>


import charts

app = Flask(__name__)

@app.route('/pie')  
def hello():
    # Generate the figure **without using pyplot**.
    fig1 = charts2.show_bar_charts()
    return render_template('notdash.html', user_image=fig1)