import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42
from matplotlib.backends.backend_pdf import PdfPages
import seaborn as sns; sns.set()
from scipy.stats import ranksums
import csv
from matplotlib.ticker import FuncFormatter
from mpl_toolkits.basemap import Basemap


"""
Load data and organize/subset 
"""
# load in song data
data_path = "C:/Users/abiga/Box " \
            "Sync/Abigail_Nicole/ChippiesTimeOfDay" \
            "/FinalChippiesDataReExportedAs44100Hz_LogTransformed_forTOD.csv"
log_song_data = pd.DataFrame.from_csv(data_path, header=0, index_col=None)

# load in time data --> before or after sunrise, twilights, and noon (only
# going to use sunrise and noon)
data_path = "C:/Users/abiga/Box " \
            "Sync/Abigail_Nicole/ChippiesTimeOfDay" \
            "/FinalChippiesDataReExportedAs44100Hz_LogTransformed" \
            "_forTOD_SunriseTwilightNoon.csv"
time_data = pd.DataFrame.from_csv(data_path, header=0, index_col=None)
# must remove duplicates -- have more than one bird from same recording --
# duplicate catalog number and time data
time_data = time_data.drop_duplicates()

# combine tables using catalog no
combined_df = pd.merge(log_song_data, time_data, on='CatalogNo')
print(combined_df.shape)
# combined_df.to_csv("C:/Users/abiga\Box "
#                    "Sync\Abigail_Nicole\ChippiesTimeOfDay\RecordingInfo"
#                    "/TimeOfDayPaper_RecordingsUsed_wData.csv", index=False)

# only keep ones with time data
combined_df = combined_df.drop(combined_df[combined_df.Sunrise ==
                                           '--'].index).copy().reset_index(
    drop=True)


""""
Geographic distribution of song duration for dawn
"""

# supplemental figure

dawn_only = combined_df[combined_df['Sunrise'] == 'before sunrise']
print(dawn_only.shape)

my_dpi = 96
fig = plt.figure(figsize=(2600 / my_dpi, 1800 / my_dpi), dpi=my_dpi,
                 frameon=False)

# make the background map
# m = Basemap(llcrnrlat=8, llcrnrlon=-169, urcrnrlat=72, urcrnrlon=-52)
m = Basemap(llcrnrlat=8, llcrnrlon=-169, urcrnrlat=72, urcrnrlon=-52, projection='merc')
m.drawcoastlines(color='k', linewidth=1.5)
m.drawcountries(color='k', linewidth=1.5)
m.drawstates(color='gray')
m.drawmapboundary(fill_color='w', color='none')

xpts_dawn, ypts_dawn = m(np.asarray(dawn_only['Longitude']), np.asarray(dawn_only['Latitude']))
m.scatter(xpts_dawn, ypts_dawn, marker='o',
          c=dawn_only['Duration of Song Bout (log(ms))'], cmap='cool',
          edgecolors='k',
          linewidth=0.5, s=200)
cb = m.colorbar()

ticks_number = []
t_old = []
for t in cb.ax.get_yticklabels():
    t_old.append(float(t.get_text()))
    new_tick = float(t.get_text().replace(t.get_text(), str(
        np.exp(float(t.get_text()))/1000)))
    ticks_number.append(new_tick)
cb.set_ticks(t_old)
cb.set_ticklabels(["%.2f" % e for e in ticks_number])
cb.ax.tick_params(labelsize=25)

plt.tight_layout()

pdf = PdfPages("C:/Users/abiga/Box "
               "Sync/Abigail_Nicole/ChippiesTimeOfDay"
               "/GeographicSpread_DawnDuration"
               ".pdf")

pdf.savefig(dpi=fig.dpi, orientation='landscape', transparent=True)
pdf.close()

plt.show()
