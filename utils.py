# import streamlit as st
# from datetime import datetime
# import yaml
# from typing import Dict, List, Union
# import re

# def validate_time_format(time_str: str) -> Union[str, bool]:
#     """
#     Validate and standardize time format.

#     Args:
#         time_str: Time string to validate

#     Returns:
#         Standardized time string in HH:MM format if valid, False otherwise
#     """
#     try:
#         # Try parsing with different formats
#         for fmt in ["%H:%M", "%I:%M", "%H:%M:%S", "%I:%M:%S"]:
#             try:
#                 parsed_time = datetime.strptime(time_str, fmt)
#                 return parsed_time.strftime("%H:%M")
#             except ValueError:
#                 continue
#         return False
#     except:
#         return False

# def validate_url(url: str) -> bool:
#     """
#     Validate URL format.

#     Args:
#         url: URL string to validate

#     Returns:
#         Boolean indicating if URL is valid
#     """
#     url_pattern = re.compile(
#         r'^https?://'  # http:// or https://
#         r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain
#         r'localhost|'  # localhost
#         r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # IP
#         r'(?::\d+)?'  # optional port
#         r'(?:/?|[/?]\S+)$', re.IGNORECASE)
#     return url_pattern.match(url) is not None

# def boolean_representer(dumper: yaml.Dumper, data: bool) -> yaml.ScalarNode:
#     """
#     Custom representer for boolean values to maintain Python capitalization.

#     Args:
#         dumper: YAML dumper instance
#         data: Boolean value to represent

#     Returns:
#         YAML scalar node with proper capitalization
#     """
#     if data:
#         return dumper.represent_scalar('tag:yaml.org,2002:bool', 'True')
#     return dumper.represent_scalar('tag:yaml.org,2002:bool', 'False')

# def generate_course_schedule_yaml(schedule_data: Dict[str, List[Dict]]) -> str:
#     """
#     Generate YAML string for course schedule.

#     Args:
#         schedule_data: Dictionary containing schedule information

#     Returns:
#         Formatted YAML string
#     """
#     # Add custom boolean representer
#     yaml.add_representer(bool, boolean_representer)

#     # Convert the data to proper format
#     formatted_data = {}
#     for day, courses in schedule_data.items():
#         if courses:  # Only include days with courses
#             formatted_data[day] = []
#             for course in courses:
#                 formatted_data[day].append({
#                     'course': course['name'],
#                     'start_time': course['start_time'],
#                     'end_time': course['end_time'],
#                     'send_message': course['send_message']
#                 })

#     return yaml.dump(formatted_data, sort_keys=False, allow_unicode=True)

# def generate_url_yaml(courses: List[str]) -> str:
#     """
#     Generate YAML string for course URLs.

#     Args:
#         courses: List of course names

#     Returns:
#         Formatted YAML string
#     """
#     url_data = {}
#     for course in courses:
#         url_value = st.session_state.url_values.get(course, '')
#         url_data[course] = url_value if url_value else 'https://example.com/course'

#     return yaml.dump(url_data, sort_keys=False, allow_unicode=True)

import streamlit as st
from datetime import datetime
import yaml
from typing import Dict, List, Union

def validate_time_format(time_str: str) -> Union[str, bool]:
    """
    Validate and standardize time format.

    Args:
        time_str: Time string to validate

    Returns:
        Standardized time string in HH:MM format if valid, False otherwise
    """
    try:
        # Try parsing with different formats
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
    """
    Custom representer for boolean values to maintain Python capitalization.

    Args:
        dumper: YAML dumper instance
        data: Boolean value to represent

    Returns:
        YAML scalar node with proper capitalization
    """
    if data:
        return dumper.represent_scalar('tag:yaml.org,2002:bool', 'True')
    return dumper.represent_scalar('tag:yaml.org,2002:bool', 'False')

def generate_course_schedule_yaml(schedule_data: Dict[str, List[Dict]]) -> str:
    """
    Generate YAML string for course schedule.

    Args:
        schedule_data: Dictionary containing schedule information

    Returns:
        Formatted YAML string
    """
    # Add custom boolean representer
    yaml.add_representer(bool, boolean_representer)

    # Convert the data to proper format
    formatted_data = {}
    for day, courses in schedule_data.items():
        if courses:  # Only include days with courses
            formatted_data[day] = []
            for course in courses:
                formatted_data[day].append({
                    'course': course['name'],
                    'start_time': course['start_time'],
                    'end_time': course['end_time'],
                    'send_message': course['send_message']  # Will now use True/False capitalization
                })

    return yaml.dump(formatted_data, sort_keys=False, allow_unicode=True)

def generate_xpath_yaml(courses: List[str]) -> str:
    """
    Generate YAML string for course xpaths.

    Args:
        courses: List of course names

    Returns:
        Formatted YAML string
    """
    xpath_data = {}
    for course in courses:
        xpath_value = st.session_state.xpath_values.get(course, '')
        xpath_data[course] = xpath_value if xpath_value else '/html/body/div[4]/div[2]/div/div/section/div/div/div/aside/section[2]/div/div/div[1]/div[2]/div/div/div[1]/div/div/div[3]/div[1]/div/div[1]/a/span[3]'

    return yaml.dump(xpath_data, sort_keys=False, allow_unicode=True)