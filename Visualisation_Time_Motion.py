from CaptureVideo_MotionDetection import data_frame
from bokeh.plotting import figure, show, output_file
from bokeh.models import HoverTool, ColumnDataSource

data_frame["Start_str"] = data_frame["Start"].dt.strftime("%Y/%m/%d %H:%M:%S")
data_frame["End_str"] = data_frame["End"].dt.strftime("%Y/%m/%d %H:%M:%S")

columd_data_source = ColumnDataSource(data_frame)

fig = figure(x_axis_type = 'datetime', height = 100, width = 500, sizing_mode = 'scale_both', title = "Detection Time")
fig.yaxis.minor_tick_line_color = None
fig.ygrid[0].ticker.desired_num_ticks = 1

hover = HoverTool(tooltips = [("Start", "@Start_str"), ("End", "@End_str")])
fig.add_tools(hover)

plott = fig.quad(left = "Start", right = "End", bottom = 0, top = 1, color = "red", source = columd_data_source)

output_file("Graph_Detection.html")
show(fig)