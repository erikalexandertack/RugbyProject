import xml.etree.ElementTree as ET
import csv
import matplotlib.pyplot as plt
from sportscode import parse_xml_file
import json
from matplotlib import style


#style.use('bmh')

def main():

    # Edit these
    
    #teams =  ['Rugby ATL','Rugby United New York']
    #teams =  ['Austin Gilgronis','Rugby United New York']
    #teams =  ['San Diego Legion','Rugby United New York']
    teams =  ['Houston Sabercats','Rugby United New York']
    #teams =  ['New England Freejacks','Rugby United New York']

    #filename =  'ATL_RUNY.xml'
    #filename =  'RUNY_AUS.xml'
    #filename =   'HOU_RUNY.xml'
    filename =   'HOU_RUNY.xml'
    #filename =   'NE_RUNY.xml'
    
    # Initialize variables
    momentum_teams_R = {t:0 for t in teams}
    momentum_teams_L = {t:0 for t in teams}
    momentum_teams = {t:0 for t in teams}
    score_lookup = get_scoring_chart()
    total_momentum = []
    total_momentum_L = []
    total_momentum_R = []

    # Parse XML file
    events = parse_xml_file(filename,teams)
    events = [e for e in events if e['team'] is not None]
    side_events = parse_xml_file(filename,teams)
    side_events = [e for e in side_events if e['team'] is not None]

    for event in events:


            # Find the event in the instance with the greatest point impact
            max_event = max(event['labels'],key=lambda l: abs(score_lookup.get(l,0)))
            max_score = score_lookup.get(max_event,0)
            momentum_teams[event['team']] += max_score

            # Look for special events for plotting
            points_scored = any(l[0] == 'Points Scored' for l in event['labels'])
            yellow_card = any(l[1] == 'Yellow Card' for l in event['labels'])

            # Calculate Running Score
            current_momentum = momentum_teams[teams[1]] - momentum_teams[teams[0]]
            
            # Update event object to add to the total momentum list
            event['current_momentum'] = current_momentum
            event['points_scored'] = points_scored
            event['yellow_card'] = yellow_card
            total_momentum.append(event)

    for event in side_events:
        y = event['y']
        time = event['start']
        field_position=event['field_lr']

        if field_position =='L':

            # Find the event in the instance with the greatest point impact
            max_event = max(event['labels'],key=lambda l: abs(score_lookup.get(l,0)))
            max_score = score_lookup.get(max_event,0)
            momentum_teams_L[event['team']] += max_score

            # Look for special events for plotting
            points_scored = any(l[0] == 'Points Scored' for l in event['labels'])
            yellow_card = any(l[1] == 'Yellow Card' for l in event['labels'])

            # Calculate Running Score
            current_momentum = momentum_teams_L[teams[1]] - momentum_teams_L[teams[0]]
            
            # Update event object to add to the total momentum list
            event['current_momentum'] = current_momentum
            event['points_scored'] = points_scored
            event['yellow_card'] = yellow_card
            total_momentum_L.append(event)

        elif field_position =='R':

            # Find the event in the instance with the greatest point impact
            max_event = max(event['labels'],key=lambda l: abs(score_lookup.get(l,0)))
            max_score = score_lookup.get(max_event,0)
            momentum_teams_R[event['team']] += max_score

            # Look for special events for plotting
            points_scored = any(l[0] == 'Points Scored' for l in event['labels'])
            yellow_card = any(l[1] == 'Yellow Card' for l in event['labels'])

            # Calculate Running Score
            current_momentum = momentum_teams_R[teams[1]] - momentum_teams_R[teams[0]]
            
            # Update event object to add to the total momentum list
            event['current_momentum'] = current_momentum
            event['points_scored'] = points_scored
            event['yellow_card'] = yellow_card
            total_momentum_R.append(event)
   
    
    
    ax1 = plt.subplot2grid((4,1), (0,0), rowspan=1, colspan=1)
    ax2 = plt.subplot2grid((4,1), (1,0), rowspan=1, colspan=1)
    ax3 = plt.subplot2grid((4,1), (2,0), rowspan=2, colspan=1)

    x,y,team_1_time, team_1_points , team_2_time, team_2_points = plot_momentum(total_momentum_R,teams)
    ax1.set_title('Right-Hand side Momentum (Full Match)')
    ax1.plot(x,y,'r')

    x,y,team_1_time, team_1_points , team_2_time, team_2_points = plot_momentum(total_momentum_L,teams)
    ax2.set_title('Left-Hand side Momentum (Full Match)')
    ax2.plot(x,y,'r')

    x,y,team_1_time, team_1_points , team_2_time, team_2_points = plot_momentum(total_momentum,teams)

    # plt.xlabel('Time')
    # plt.ylabel('Momentum')
    # ax3.set_title('RUNY HOU Full Momentum')
    # ax3.plot(team_1_time,team_1_points,'s',color='orange', label='RUNY Score')
    # ax3.plot(team_2_time,team_2_points,'s',color='red',label='HOU Score')
    # ax3.legend()
    # ax3.plot(x,y,'blue')

    #plt.subplots_adjust(wspace=6)
    # plt.tight_layout(rect=[0, 0, 1, 0.95])
    # #plt.show()
    # plt.savefig('RugbyHOU.png')
    print(total_momentum[1])

def plot_momentum(tot_momentum,teams):
    time = [e['start'] for e in tot_momentum]
    momentum = [e['current_momentum'] for e in tot_momentum]

    team_1_time = [e['start'] for e in tot_momentum if e['team'] == teams[0] and e['points_scored']]
    team_1_points = [e['current_momentum'] for e in tot_momentum if e['team'] == teams[0] and e['points_scored']]
    #plt.plot(team_1_time,team_1_points,'s',color='orange')

    team_2_time = [e['start'] for e in tot_momentum if e['team'] == teams[1] and e['points_scored']]
    team_2_points = [e['current_momentum'] for e in tot_momentum if e['team'] == teams[1] and e['points_scored']]
    #plt.plot(team_2_time,team_2_points,'s',color='red')
    
    return  time, momentum, team_1_time, team_1_points , team_2_time, team_2_points 


def print_to_csv(events):
    with open('output.csv','w') as fout:
        wr = csv.writer(fout)
        wr.writerow(['start','end','game_clock','code','group','text'])
        for event in events:
            wr.writerow(event)

def get_scoring_chart():
    base_carry = 1
    base_kick = 5
    turnover = 15
    yellow_card = 30
    penalty = 20
    conversion = 20
    kick_at_goal = 25
    try_scored = 50
    lineout = 3
    maul = 5
    catch = 3
    base_pass = 2
    ruck = 1
    scrum = 3
    tackle = 2

    return {
        ('Ball Carry', '30-40m - Metres Gained'): base_carry*20,
        ('Ball Carry', '2-5m - Metres Gained'): base_carry*2,
        ('Ball Carry', 'Ball Carry Quality - Ineffective'): -base_carry,
        ('Ball Carry', '5-10m - Metres Gained'): base_carry*3,
        ('Ball Carry', 'Line Break'): base_carry*10,
        ('Ball Carry', 'Ball Carry Quality - Effective'): base_carry,
        ('Ball Carry', '0-2m - Metres Gained'): base_carry,
        ('Ball Carry', '20m-30m - Metres Gained'): base_carry*10,
        ('Ball Carry', '10-20m - Metres Gained'): base_carry*5,
        ('Ball Carry', 'Ball Carry Quality - Turnover Ineffective'): -turnover,
        ('Ball In Play', 'Ball in Play - Lineout'): 0,
        ('Ball In Play', 'Ball in Play - Scrum'): 0,
        ('Ball In Play', 'Ball in Play'): 0,
        ('Ball Steal', 'Ball Steal - Ruck'): turnover,
        ('Ball Steal', 'Ball Steal - Tackle'): turnover,
        ('Ball Steal', 'Ball Steal - Set Piece'): turnover,
        ('Cards', 'Yellow Card'): -yellow_card,
        ('Catch', 'Catch Quality - Won Possession'): 10,
        ('Catch', 'Catch Quality - Turnover Ineffective'): -turnover,
        ('Catch', 'Catch Quality - Ineffective'): -catch,
        ('Catch', 'Catch Quality - Effective'): catch,
        ('Conversion', 'Conversion - Made'): conversion,
        ('Conversion', 'Conversion - Total'): conversion,
        ('Counter Attack', 'Counter Attack - From Kick'): 0,
        ('Free Kick', 'Fair Catch'): 0,
        ('Free Kick', 'Free Kick'): 0,
        ('Free Kick Conceded', 'Free Kick Conceded'): -turnover,
        ('Free Kick Infringement', 'Free Kick Infringement Reason - Not Taking Hit'): 0,
        ('Free Kick Infringement', 'Free Kick Infringement - Others'): 0,
        ('Free Kick Infringement', 'Free Kick Infringement Reason - Closing Gap'): 0,
        ('Free Kick Infringement', 'Free Kick Infringement Reason - Others'): 0,
        ('Free Kick Infringement', 'Free Kick Infringement Reason - Early Push'): 0,
        ('Free Kick Infringement', 'Free Kick Infringement - Lineout'): 0,
        ('Free Kick Infringement', 'Free Kick Infringement - Scrum'): 0,
        ('Gainline', 'Gainline Neutral'): base_carry,
        ('Gainline', 'Gainline Lost'): -base_carry,
        ('Gainline', 'Gainline +'): base_carry*2,
        ('Gainline', 'Gainline -'): -base_carry*2,
        ('Gainline', 'Gainline Over'): base_carry,
        ('Handling Error', 'Handling Error'): -5,
        ('Kick', '10-20m - Metres Gained'): 0,
        ('Kick', 'Territory Kick'): 0,
        ('Kick', 'Short Kick Result - Effective'): base_kick,
        ('Kick', '20m-30m - Metres Gained'): base_kick*2,
        ('Kick', '0-2m - Metres Gained'): -base_kick,
        ('Kick', 'Long Kick Result - Turnover Effective'): base_kick*3,
        ('Kick', 'Short Kick'): 0,
        ('Kick', '40m+ - Metres Gained'): base_kick*4,
        ('Kick', '2-5m - Metres Gained'): -base_kick,
        ('Kick', '30-40m - Metres Gained'): base_kick*3,
        ('Kick', 'Long Kick Result - Turnover Ineffective - Out On Full'): -base_kick,
        ('Kick', 'Long Kick Result - Turnover Ineffective'): -base_kick,
        ('Kick', 'Short Kick Result - Turnover Ineffective'): -base_kick,
        ('Kick', 'Short Kick Result - Ineffective'): 0,
        ('Kick', 'Touch Kick'): 0,
        ('Kicks at Goal Result', 'Kicks at Goal - Made'): kick_at_goal,
        ('Kicks at Goal Result', 'Kicks at Goal - Missed'): 0,
        ('Lineout', 'Lineout - Effective'): lineout,
        ('Lineout', 'Lineout - 5 Man'): 0,
        ('Lineout', 'Lineout - Ineffective'): 0,
        ('Lineout', 'Lineout - 5 + 1'): 0,
        ('Lineout', 'Lineout - 6 + 1'): 0,
        ('Lineout', 'Lineout - Turnover Ineffective'): -lineout*3,
        ('Lineout', 'Lineout - Full'): 0,
        ('Lineout', 'Lineout - 4 Man'): 0,
        ('Lineout', 'Lineout - 6 Man'): 0,
        ('Maul', 'Maul - Turnover'): -maul*2,
        ('Maul', 'Maul - Retained'): maul,
        ('Pass', 'Other Pass - Effective'): base_pass,
        ('Pass', 'Other Pass - Turnover Ineffective'): -turnover,
        ('Pass', 'Offload - Turnover Ineffective'): -turnover,
        ('Pass', 'Offload - Effective'): base_pass,
        ('Pass', 'Offload - Ineffective'): 0,
        ('Pass', 'Other Pass - Ineffective'): 0,
        ('Penalty Infringement', 'Penalty Infringement Reason - Other'): -penalty,
        ('Penalty Infringement', 'Penalty Infringement Reason - High Tackle'): -penalty,
        ('Penalty Infringement', 'Penalty Infringement - Tackle'): -penalty,
        ('Penalty Infringement', 'Penalty Infringement Reason - A Defender'): -penalty,
        ('Penalty Infringement', 'Penalty Infringement - Maul'): -penalty,
        ('Penalty Infringement', 'Penalty Conceded'): -penalty,
        ('Penalty Infringement', 'Penalty Infringement Reason - Taking Out - Obstruction'): -penalty,
        ('Penalty Infringement', 'Penalty Infringement - Ruck'): -penalty,
        ('Penalty Infringement', 'Penalty Infringement - Foul Play'): -penalty,
        ('Penalty Infringement', 'Penalty Infringement Reason - Entry'): -penalty,
        ('Penalty Infringement', 'Penalty Infringement Reason - Not Rolling Away'): -penalty,
        ('Penalty Infringement', 'Penalty Infringement Reason - Charging'): -penalty,
        ('Penalty Infringement', 'Penalty Infringement Reason - Not Releasing'): -penalty,
        ('Penalty Infringement', 'Penalty Infringement Reason - Collapsing'): -penalty,
        ('Penalty Infringement', 'Penalty Infringement - Lineout'): -penalty,
        ('Penalty Infringement', 'Penalty Infringement - Scrum'): -penalty,
        ('Penalty Infringement', 'Penalty Infringement - Offside'): -penalty,
        ('Penalty Infringement', 'Penalty Infringement Reason - Boring In'): -penalty,
        ('Penalty Infringement', 'Penalty Infringement Reason - Stapling Off - Defence'): -penalty,
        ('Penalty Infringement', 'Penalty Infringement Reason - Backline'): -penalty,
        ('Penalty Infringement', 'Penalty Infringement Reason - Standing Up'): -penalty,
        ('Penalty Shot', 'Penalty Shot - Missed'): 0,
        ('Penalty Shot', 'Penalty Shot - Made'): kick_at_goal,
        ('Penalty Shot', 'Penalty Shot - Total'): 0,
        ('Penalty Start', 'Tap Penalty'): 0,
        ('Penalty Start', 'Penalty Kick - Effective'): base_kick*3,
        ('Points Scored', 'Conversion'): conversion,
        ('Points Scored', 'Try'): try_scored,
        ('Points Scored', 'Penalty Shot'): kick_at_goal,
        ('Points Scored', 'Penalty Try'): try_scored,
        ('Ruck', 'Ruck - Retained'): ruck,
        ('Ruck', 'Ruck - Slow'): -ruck*2,
        ('Ruck', 'Ruck - Fast'): ruck*2,
        ('Ruck', 'Ruck - Not Completed'): 0,
        ('Scrum', 'Scrum - Pre-Ball stability'): 0,
        ('Scrum', 'Scrum - Completed'): 0,
        ('Scrum', 'Scrum - Reset'): 0,
        ('Scrum', 'Scrum - Popped'): 0,
        ('Scrum', 'Scrum - Effective'): scrum,
        ('Scrum', 'Scrum - Turnover Ineffective'): 0,
        ('Scrum', 'Scrum - Turnover'): 0,
        ('Scrum', 'Scrum - Collapsed'): 0,
        ('Scrum', 'Scrum - Free Kick'): 0,
        ('Scrum', 'Scrum - Pre-Engage'): 0,
        ('Scrum', 'Scrum - Penalty'): 0,
        ('Start 22', 'Start 22 - Turnover'): 0,
        ('Start 22', 'Start 22 - Short'): 0,
        ('Start Half', 'Start Half - Long'): 0,
        ('Start Half', 'Start Half - Regained'): turnover,
        ('Start Half', 'Start Half - Turnover'): -turnover,
        ('Start Half', 'Start Half - Short'): 0,
        ('Stoppages', 'Stoppages - Held Up Ingoal'): 0,
        ('Stoppages', 'Stoppages - Ball Lost Forward'): -turnover,
        ('Stoppages', 'Stoppages - Unplayable from Kick'): 0,
        ('Stoppages', 'Stoppages - Forward Pass'): -5,
        ('Stoppages', 'Stoppages - Unplayable'): 0,
        ('Stoppages', 'Stoppages - Knock On'): -turnover,
        ('Tackle', 'Quality - Ball Control Lost'): tackle*2,
        ('Tackle', 'Active Tackle'): tackle,
        ('Tackle', 'Quality - Made Tackle'): tackle,
        ('Tackle', 'Quality - Impeded Progress'): tackle*2,
        ('Tackle', 'Try Saver Tackle'): tackle*3,
        ('Tackle', 'Quality - Turnover Tackle'): turnover,
        ('Tackle', 'Quality - Missed Tackle'): -tackle*2,
        ('Tackle', 'Quality - Dominant Tackle'): tackle*4,
        ('Tackle', 'Assist Tackle'): 0,
        ('Turnover Conceded', 'Turnover Conceded'): -turnover
    }


if __name__ == '__main__':
    main()