from sportscode import parse_xml_file
import json


def main():
    teams = ['Rugby United New York','Houston Sabercats']
    filename = 'HOU_RUNY.xml'

    # Parse XML file
    events = parse_xml_file(filename,teams)


    #Need to use this in order to solve
    player_events = {}
    for event in events:
        player_name = event['player']
        if player_name not in player_events:
            player_events[player_name] = []
            player_events[player_name].append(event)
        else:
            player_events[player_name].append(event)
        

    # for player_name,events in player_events.items():
    #     print(player_name,len(events))

    #To See Data
    print(json.dumps(events[0:200],indent=4))

main()
