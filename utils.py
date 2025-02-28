import yaml
from datetime import datetime
from typing import Dict, List, Union

def validate_time_format(time_str: str) -> Union[str, bool]:
    try:
        for fmt in ["%H:%M", "%I:%M", "%H:%M:%S", "%I:%M:%S"]:
            try:
                parsed_time = datetime.strptime(time_str, fmt)
                return parsed_time.strftime("%H:%M")
            except ValueError:
                continue
        return False
    except:
        return False

def boolean_representer(dumper: yaml.Dumper, data: bool) -> yaml.ScalarNode:
    if data:
        return dumper.represent_scalar('tag:yaml.org,2002:bool', 'True')
    return dumper.represent_scalar('tag:yaml.org,2002:bool', 'False')

def generate_course_schedule_yaml(schedule_data: Dict[str, List[Dict]]) -> str:
    yaml.add_representer(bool, boolean_representer)
    formatted_data = {}
    for day, courses in schedule_data.items():
        if courses:
            formatted_data[day] = []
            for course in courses:
                formatted_data[day].append({
                    'course': course['name'],
                    'start_time': course['start_time'],
                    'end_time': course['end_time'],
                    'send_message': course['send_message']
                })
    return yaml.dump(formatted_data, sort_keys=False, allow_unicode=True)

def generate_url_yaml(url_values: Dict[str, str]) -> str:
    return yaml.dump(url_values, sort_keys=False, allow_unicode=True)