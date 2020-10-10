from sportscode import parse_xml_file
from test import draw_pitch
import matplotlib.pyplot as plt
import numpy as np
import json
import xml.etree.ElementTree as ET
import seaborn as sns

#You will haveto specify the game and the player and time period


#plt.show()

def main():
    teams = ['Rugby United New York','Houston SaberCats']
    filename = 'HOU_RUNY.xml'
    count=0
    
    # Parse XML file
    events = parse_xml_file(filename,teams)
    
    plt.ion() # Interactive mode on
    label_blacklist = get_label_blacklist(teams)
    print(label_blacklist)

    for e in events:
        labels = e['labels']
        x = e['x']
        y = e['y']
        
        if x and y and labels:
            #if e['field_lr']=='R':
            if e['code']=='Connor Wallace-Sims':
                maxcount=500

                x = int(x)
                y = int(y)
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
                plt.plot(x,y,'o')
                plt.show()

            

            
                count += 1
                if count == maxcount:
                    break



def get_event_label(labels,blacklist):
    label = next((l[0] for l in labels if l[0] not in blacklist),None)

    return label

def get_label_blacklist(teams):
    blacklist = {
        'Game Clock',
        'Phase Number',
        'Field Area',
        'Field L-R',
        'X',
        'Y',
        'Post-Tackle Assessment'
    }
    blacklist.add(teams[0])
    blacklist.add(teams[1])

    return blacklist

def _get_xml_root(fname):
    tree = ET.parse(fname)
    root = tree.getroot()

    return root


if __name__ == '__main__':
    fig=plt.figure()

    fig.set_size_inches(7, 5)
    ax=fig.add_subplot(1,1,1)
    
    main()

    
