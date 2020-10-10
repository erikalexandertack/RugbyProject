import matplotlib.pyplot as plt
import json
from pandas.io.json import json_normalize
import numpy as np
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Arc, Rectangle, ConnectionPatch
from matplotlib.offsetbox import  OffsetImage
import squarify
from functools import reduce

def draw_pitch(ax):
    # size of the pitch is 120, 80
    #Create figure

    #Pitch Outline & Trylines
    plt.plot([0,0],[0,700], color="black")#Ltry
    plt.plot([-150,-150],[0,700], color="black")#Ldeadball
    plt.plot([-150,1150],[700,700], color="black")#sidelineA
    plt.plot([1000,1000],[700,0], color="black")#Rtry
    plt.plot([1150,-150],[0,0], color="black")#SidelineB
    plt.plot([1150,1150],[0,700], color="black")#Rdeadball

    #50, 22's, 5m 
    plt.plot([220,220],[0,700], color="black",)#L22
    plt.plot([770,770],[0,700], color="black",)#R22
    plt.plot([500,500],[0,700], color="black")#50m

    #Dashes, and text for 5 and 15m's
    plt.plot([525,475],[150,150], color="black",linestyle=(0, (10, 25)))#15mB
    plt.plot([525,475],[550,550], color="black",)#15mA
    plt.plot([195,245],[550,550], color="black",)#15mA
    plt.plot([745,795],[550,550], color="black",)#15mA
    plt.plot([195,245],[150,150], color="black",)#15mB
    plt.plot([745,795],[150,150], color="black",)#15mB
    plt.plot([950,50],[650,650], color="black",linestyle=(0, (15, 20)))#5mA
    plt.plot([950,50],[50,50], color="black",linestyle=(0, (15, 20)))#5mB
    plt.plot([50,50],[0,700], color="black",linestyle=(0, (15, 25)), linewidth=1)
    plt.plot([950,950],[0,700], color="black", linestyle=(0, (15, 25)), linewidth=1)
    ax.text(175, 155, r'2 2', fontsize=15) #L22 text
    ax.text(725, 155, r'2 2', fontsize=15) #R22 text
    ax.text(450, 155, r'5 0', fontsize=15) #50 text
    plt.plot([600,600],[0,700], color="black",linestyle=(0, (15, 25)), linewidth=1)#
    plt.plot([400,400],[0,700], color="black", linestyle=(0, (15, 25)), linewidth=1)
    

    #Goalposts
    plt.plot([0,0],[310,380], color="red",linewidth=5)#Lpost
    plt.plot([1000,1000],[310,380], color="red",linewidth=5)#Rtry



fig=plt.figure()
fig.set_size_inches(7, 5)
ax=fig.add_subplot(1,1,1)
draw_pitch(ax)
plt.show()

