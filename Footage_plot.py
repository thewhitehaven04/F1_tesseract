from Footage_OCR import Parse_Data
from matplotlib import pyplot as plt
import numpy as np


class Footage_Plot():

    teamcolors = {'Mercedes': 'turquoise', 'Ferrari': 'red',
                  'Red Bull': 'midnightblue', 'McLaren': 'darkorange',
                  'Renault': 'yellow', 'Racing Point': 'magenta',
                  'Alpha Tauri': 'black', 'Alfa Romeo': 'firebrick',
                  'Haas': 'gray', 'Williams': 'cyan'}

    def __init__(self, parse_object, driver_name,
                 team_name, gp, position, fps=30):
        self.driver_name = driver_name
        self.team_name = team_name
        self.gp = gp
        self.position = position
        self.interval = parse_object.sample_rate/fps
        self.speed_values = self._get_speed_values(parse_object)
        self.distance_values = self._get_distance_values()

    def _get_speed_values(self, parse_object):
        try:
            str_speed_list = parse_object.speed_list
        except Exception:
            print("The parse object has no 'speed_list' property.")
        else:
            print('The speed list has been succesfully acquired.')
        int_speed_list = Footage_Plot._populate_array(str_speed_list)
        avg_speed_list = Footage_Plot._avg_speeds(int_speed_list)
        return avg_speed_list

    def _populate_array(arr):
        """Convert the recognized values from str to int.
        If the value is not recognized properly,
        set the corresponding value to zero"""
        arr_2 = []
        for entry in arr:
            if entry.isdecimal():
                arr_2.append(entry)
            else:
                arr_2.append(0)
        return np.array(arr_2, dtype=np.uint16)

    def _get_distance_values(self):
        """Get the distance of the lap based on average speeds multiplied
        by frame times, calculated as 1/fps"""
        data = self.speed_values
        avgs = []
        for i in range(len(data)):
            if avgs:
                avg = self.interval*data[i]*1000/3600+avgs[i-1]
                avgs.append(avg)
            else:
                avg = self.interval*data[i]*1000/3600
                avgs.append(avg)
        return np.array(avgs, dtype=np.float16)

    def _avg_speeds(speeds):
        avgspeeds = []
        for i in range(len(speeds)-1):
            avgspeeds.append(0.5*(speeds[i+1]+speeds[i]))
        return np.array(avgspeeds, np.float16)

    def _interpolate_values(dist, speeds):
        for i in range(1,len(speeds)-1):
            prev = speeds[i-1]
            curr = speeds[i]
            succ = speeds[i+1]
            if np.abs(curr-prev)>10 or np.abs(succ-curr):
                speeds[i]=0.5*(speeds[i-7]+speeds[i+7])
        return speeds

    def plot(self, ax):
        x = self.distance_values
        y = Footage_Plot._interpolate_values(x, self.speed_values)
        color = Footage_Plot.teamcolors[self.team_name]
        ax.plot(x, y, lable=self.driver_name, color=color)

class Multiplot():

    def __init__(self, dim, dpi, footage_plots):
        self.fig = plt.Figure(dpi=dpi, figsize=dim)
        self.footage_plots = footage_plots
        self.axs = []

    def add_axes(self, x0=0, y0=0, x1=1, y1=1):
        self.axs.append(self.fig.add_axes([x0,y0,x1,y1]))

    def multiplot(self, plot_id):
        names = [ft_plot.driver_name for ft_plot in self.footage_plots]
        self.axs[plot_id].legend(labels = tuple(names),
                                loc = 'lower right')
        self.axs[plot_id].set_xlabel('Distance, m')
        self.axs[plot_id].set_ylabel('Speed, kp/h')
        self.axs[plot_id].set_yticks(np.linspace(0, 350, num = 36))
        self.axs[plot_id].set_ylim([0, 360])
        for plot in self.footage_plots:
            plot.plot(self.axs[plot_id])
        self.axs[plot_id].legend()
        self.fig.savefig(r'./test.png')

if __name__ == '__main__':
    Hamilton, Verstappen = Parse_Data('P02_Hamilton_Russia', 1717, 2317, sample_rate = 2), Parse_Data('P04_Verstappen_Russia', 1736, 2336, sample_rate = 2)
    Hamilton.get_list_of_speeds()
    Verstappen.get_list_of_speeds()
    plot_Hamilton = Footage_Plot(Hamilton, 'Hamitlon', 'Mercedes', 'Russia', 2, fps=25)
    plot_Verstappen = Footage_Plot(Verstappen, 'Verstappen', 'Red Bull', 'Russia', 4, fps=25)
