import csv
import matplotlib.pyplot as plt


def work_calculation (f):
  data = []
  with open(f,'r') as fin:
      rd = csv.reader(fin)
      for row in rd:
          data.append(row)

  #seperate header , difficulties calculating with strings included
  header = data[0]
  data.pop(0)

  #create variables
  teamRUNY = []
  opponent = []
  runy_key = [] #create dictionary for runy and opponents
  opp_key = []
  runy_olist = [] 
  runy_dlist = []
  opp_olist= []
  opp_dlist = []

  #split team
  for i in data:
      if (i[0] == 'Rugby United New York'):
          teamRUNY.append(i) 
      else:
          opponent.append(i)

          
  #offensive work function
  def offense(pos):
      x = pos
      ballCarries = int(x[6]) * .5
      ballCarryMetres = int(x[7]) * .04
      linebreaks = int(x[8]) * .3
      tackleBreaks = int(x[9]) * .2
      offloads = int(x[10]) * .02
      gainlineMade_percent = int(x[11])  
      attRMArrivals = int(x[16]) *.2
      lineoutTakes = int(x[24]) * .1
      
      work =  (ballCarries+ ballCarryMetres + lineoutTakes + attRMArrivals + offloads + tackleBreaks + linebreaks)/100
      return work

  #defensive work function
  def defense(pos):
      x = pos
      madeTackles = int(x[12]) * .5 
      missedTackles =int(x[13]) * .08 
      madeTackle_percent =int(x[14])
      breakdownSteals =int(x[15]) * .1
      defRMArrivals =int(x[18]) * .3
      lineoutSteals =int(x[25]) * .1
      
      work =  (madeTackles-missedTackles+breakdownSteals+defRMArrivals+lineoutSteals)/10
      return work


  def key_maker(team,team_key): 
      x = 0
      for i in team:
          name = i[2]
          pos = i[1]
          team_key.append([name, pos])
          x+=1

  #create keys
  key_maker(teamRUNY,runy_key)
  key_maker(opponent, opp_key)


  #loop through offensive function to return calculation for both teams
  def work_calc(team,list1,list2):
      print('Entering work_calc function with:')
      print('Team=',team)
      print('list1=',list1)
      print('list2=',list2)
      index = 0
      for i in team: 
          list1.append(offense(i))
          list2.append(defense(i))
          index +=1
      print('exiting work_calc with')
      print('Team=',team)
      print('list1=',list1)
      print('list2=',list2)
          
  work_calc(teamRUNY,runy_olist, runy_dlist)
  work_calc(opponent, opp_olist, opp_dlist)

  runy_names= []
  opponent_names = []

  t=0
  def nameList(team,n_list):
      for i in team:
          n_list.append(i[2])
          
  nameList(teamRUNY, runy_names)
  nameList(opponent, opponent_names)
  
  #calculate total individual work
  indi_runyP = []
  indi_oppP = []
  
  def indi_calc (team,list1,list2,tList):
    for i in team:
      keySum = list1 + list2
      tList.append(keySum) 

  indi_calc(teamRUNY,runy_olist,runy_dlist,indi_runyP)
  indi_calc(opponent,opp_olist,opp_dlist,indi_oppP)


  #calculate team work
  teamsum = sum(runy_olist) + sum(runy_dlist)
  oppsum = sum(opp_olist) + sum(opp_dlist)

  print ("team total sum for "+str(teamRUNY[0][0])+" is " + str(teamsum))
  print ("team total sum for "+str(opponent[0][0])+" is " + str(oppsum)+"\n")

  #plot the values
  #x1 = runy_names
  #x2 = opponent_names
  #y1 = indi_runyP
  #y2 = indi_oppP
  

  #plt.bar(x1,y1)
  #plt.bar(x2,y2)

  #plt.title('Runy Work Rate')
  #plt.xlabel('Players')
  #plt.ylabel('Work rate')


  #plt.show()

game =[
  'wk1_runy_ne.csv', 
  'wk2_runy_aus.csv', 
  'wk3_runy_atl.csv', 
  'wk4_runy_hou.csv',
  'wk5_runy_sd.csv']

#work_calculation(game[0])
for i in game:
  work_calculation(i)
  

