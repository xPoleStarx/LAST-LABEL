import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backend_bases import MouseEvent
from matplotlib.widgets import Cursor

class MultiAnnotatedCursor(Cursor):
    def __init__(self, lines, ax, subsetdf, useblit=True):
        self.active = True
        self.lines = lines
        self.texts = []
        self.offset = np.array([10, 10])
        self.subsetdf = subsetdf  # Add the subsetdf DataFrame
        super().__init__(ax, horizOn=False, color='red', linewidth=0.5, useblit=useblit)
        
        for i, line in enumerate(lines):
            text = self.ax.text(
                self.ax.get_xbound()[0],
                self.ax.get_ybound()[0],
                "",
                animated=bool(self.useblit),
                visible=False, color=line.get_color())
            text.set_gid('cursor_annotation')  # Set a unique label
            self.texts.append(text)

    def set_position(self, xpos, ypos):
        coords = []
        labels = []  # Store labels for each line
        for line in self.lines:
            xdata = line.get_xdata()
            ydata = line.get_ydata()
            pos = xpos
            data = xdata
            lim = self.ax.get_xlim()
            if pos is not None and lim[0] <= pos <= lim[-1]:
                index = np.searchsorted(data, pos)
                # Adjust to check both nearby points
                if 0 < index < len(data):
                    left = abs(data[index-1] - pos)
                    right = abs(data[index] - pos)
                    if left < right:
                        coords.append(ydata[index-1])
                    else:
                        coords.append(ydata[index])
                elif index == 0:
                    coords.append(ydata[0])
                else:
                    coords.append(None)
            else:
                coords.append(None)
            labels.append(None)  # Initialize labels with None

        for j, line in enumerate(self.lines):
            if coords[j] is not None:
                # Get the index of the x-coordinate in the dataframe
                index = np.searchsorted(self.subsetdf.index, xpos)
                # Check the label at this index in the dataframe
                labels[j] = self.subsetdf['label'].iloc[index] if 0 <= index < len(self.subsetdf) else None      

        return coords, labels  # Return both coords and labels


    def onmove(self, event):
        if not self.active:
            for text in self.texts:
                text.set_visible(False)
            return
        if self.ignore(event):
            return
        if not self.canvas.widgetlock.available(self):
            return
        if event.inaxes != self.ax:
            return
        
        labels = ['CO2: ', 'O2: ', 'Temp: ']
        plotpoints, label_values = self.set_position(event.xdata, event.ydata)

        for i, (plotpoint, label, text, line) in enumerate(zip(plotpoints, label_values, self.texts, self.lines)):
            if not line.get_visible():
                text.set_visible(False)
                continue
            
            if plotpoint is not None:
                temp = [event.xdata, plotpoint]
                temp = self.ax.transData.transform(temp)
                temp = temp + self.offset + np.array([0, 10 * i])
                temp = self.ax.transData.inverted().transform(temp)
                text.set_position(temp)
                text.set_text(f"{labels[i]}{plotpoint:.2f} - Label: {label}")  # Display the label
                text.set_visible(True)
            else:
                text.set_visible(False)

        super().onmove(event)
        
        if self.useblit:
            for text in self.texts:
                if text.get_visible():
                    self.ax.draw_artist(text)
            self.canvas.blit(self.ax.bbox)
        else:
            self.canvas.draw_idle()

