import xml.etree.ElementTree as ET

def parse_xml_file(fname,teams):
    
    root = _get_xml_root(fname)
    player_map = _generate_player_map(root,teams)

    instances = {}
    for instance in _instance_iterator(root):
        instance_dict = _parse_instance(instance)

        labels = []
        for label in _label_iterator(instance):
            group = label.find('group').text
            text = label.find('text').text
            if group == 'Game Clock':
                instance_dict['game_clock'] = text
            elif group in teams:
                instance_dict['team'] = group
                instance_dict['player'] = text
            elif group == 'X':
                instance_dict['x'] = int(text)
            elif group == 'Y':
                instance_dict['y'] = int(text)
            elif group == 'Field Area':
                instance_dict['field_area'] = text
            elif group == 'Field L-R':
                instance_dict['field_lr'] = text
            else:
                labels.append((group,text))

        if instance_dict['team'] is None:
            for team_name, players in player_map.items():
                if instance_dict['code'] in players:
                    instance_dict['team'] = team_name

        instance_dict['labels'] = labels

        instances[instance_dict['iid']] = instance_dict
    
    events = [v for k,v in instances.items()]
    events = sorted(events,key=lambda e: e['start'])

    return events

def _generate_player_map(root,teams):
    player_map = {teams[0]:[],teams[1]:[]}
    for instance in _instance_iterator(root):
        for label in _label_iterator(instance):
            group = label.find('group').text
            text = label.find('text').text
            if group in teams:
                team = group
                player = text
                player_map[team].append(player)
    player_map = {k:set(v) for k,v in player_map.items()}

    return player_map

def _get_xml_root(fname):
    tree = ET.parse(fname)
    root = tree.getroot()

    return root

def _instance_iterator(root):
    for all_instances in root.iter('ALL_INSTANCES'):
        for instance in all_instances.iter('instance'):
            yield instance

def _label_iterator(instance):
    for label in instance.iter('label'):
        yield label

def _parse_instance(instance):
    iid = instance.find('ID').text
    start = instance.find('start').text
    end = instance.find('end').text
    code = instance.find('code').text

    instance_dict = {
        'start': float(start),
        'end': float(end),
        'code': code,
        'iid': iid,
        'game_clock': None,
        'team': None,
        'player': None,
        'x': None,
        'y': None,
        'field_lr': None,
        'field_area': None
    }

    return instance_dict
