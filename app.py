import streamlit as st
import yaml
from utils import validate_time_format, generate_course_schedule_yaml, generate_xpath_yaml

def main():
    st.set_page_config(page_title="Course Schedule YAML Generator", layout="wide")

    st.title("Course Schedule YAML Generator")
    st.markdown("""
    Generate YAML files for course schedules and XPath mappings.
    Choose an option below to get started.
    """)

    # Two columns for the main buttons
    col1, col2 = st.columns(2)

    with col1:
        if st.button("Create Course Schedule YAML", use_container_width=True):
            st.session_state.active_section = "schedule"

    with col2:
        if st.button("Create Course Url YAML", use_container_width=True):
            st.session_state.active_section = "xpath"

    # Initialize session state for courses and schedule
    if 'courses' not in st.session_state:
        st.session_state.courses = []  # Changed from set to list
    if 'schedule' not in st.session_state:
        st.session_state.schedule = {
            'Monday': [], 'Tuesday': [], 'Wednesday': [],
            'Thursday': [], 'Friday': []
        }
    if 'active_section' not in st.session_state:
        st.session_state.active_section = None
    if 'xpath_values' not in st.session_state:
        st.session_state.xpath_values = {}

    # Course Schedule YAML Section
    if st.session_state.active_section == "schedule":
        st.header("Course Schedule Generator")

        # Course input form in a container for better organization
        with st.container():
            st.subheader("Add New Course")
            with st.form("course_form"):
                day = st.selectbox("Select Day", 
                                  ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'])
                course_name = st.text_input("Course Name *", help="This field is required")
                col1, col2 = st.columns(2)
                with col1:
                    start_time = st.text_input("Start Time (HH:MM) *", placeholder="12:05")
                with col2:
                    end_time = st.text_input("End Time (HH:MM) *", placeholder="13:05")

                # Changed checkbox to selectbox with default False
                send_message = st.selectbox("Send Message", 
                                            options=[False, True],
                                            index=0,
                                            format_func=lambda x: str(x))

                if st.form_submit_button("Add Course"):
                    if not all([course_name, start_time, end_time]):
                        st.error("Please fill in all fields")
                    else:
                        valid_start = validate_time_format(start_time)
                        valid_end = validate_time_format(end_time)

                        if not valid_start or not valid_end:
                            st.error("Invalid time format. Please use HH:MM format (e.g., 12:05)")
                        else:
                            if course_name not in st.session_state.courses:
                                st.session_state.courses.append(course_name)
                            st.session_state.schedule[day].append({
                                'name': course_name,
                                'start_time': valid_start,
                                'end_time': valid_end,
                                'send_message': send_message
                            })
                            st.success(f"Added {course_name} to {day}")

        st.subheader("Current Schedule")
        for day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']:
            if st.session_state.schedule[day]:
                with st.expander(f"{day} ({len(st.session_state.schedule[day])} courses)", expanded=True):
                    for idx, course in enumerate(st.session_state.schedule[day]):
                        col1, col2, col3 = st.columns([3, 1, 1])
                        with col1:
                            st.write(f"📚 {course['name']}: {course['start_time']} - {course['end_time']} | Notifications: {'✅' if course['send_message'] else '❌'}")
                        with col3:
                            if st.button(f"Remove", key=f"remove_{day}_{idx}"):
                                course_name = course['name']
                                # Remove course from schedule
                                st.session_state.schedule[day].pop(idx)

                                # Check if course exists in other days
                                is_used = False
                                for other_day, courses in st.session_state.schedule.items():
                                    if any(c['name'] == course_name for c in courses):
                                        is_used = True
                                        break

                                # If course is not used anywhere else, remove from courses list and xpath values
                                if not is_used:
                                    if course_name in st.session_state.courses:
                                        st.session_state.courses.remove(course_name)
                                    if course_name in st.session_state.xpath_values:
                                        del st.session_state.xpath_values[course_name]
                                st.rerun()
                    st.divider()
            else:
                st.info(f"No courses scheduled for {day}")

        # Generate and download YAML
        if any(courses for courses in st.session_state.schedule.values()):
            if st.button("Generate Schedule YAML"):
                yaml_content = generate_course_schedule_yaml(st.session_state.schedule)
                st.download_button(
                    label="Download Schedule YAML",
                    data=yaml_content,
                    file_name="course_details.yaml",
                    mime="text/yaml"
                )

    # XPath YAML Section
    elif st.session_state.active_section == "xpath":
        st.header("Course Url Generator")
        st.info("Note: Course names must match exactly with those used in the course schedule YAML file.")

        with st.form("xpath_form"):
            # Check if there are any courses added to the schedule
            if not st.session_state.courses:
                st.warning("Please add courses in the Course Schedule section first.")
                course_name = st.text_input("Course Name", disabled=True)
                xpath_value = st.text_area("Course Url", disabled=True)
                st.form_submit_button("Add Course", disabled=True)
            else:
                course_name = st.selectbox(
                    "Select Course",
                    options=st.session_state.courses,
                    help="Select from courses already added to the schedule"
                )
                xpath_value = st.text_area("Course Url", 
                                       placeholder="https://lms.iiitkottayam.ac.in/course/view.php?id=444",
                                       help="Enter the course Url here")

                if st.form_submit_button("Add Course"):
                    if not xpath_value:
                        st.error("Please enter the XPath value")
                    else:
                        st.session_state.xpath_values[course_name] = xpath_value
                        st.success(f"Added XPath for {course_name}")

        if st.session_state.courses:
            st.subheader("Current Courses")
            courses_to_remove = []
            for i, course in enumerate(st.session_state.courses):
                col1, col2, col3 = st.columns([2, 2, 1])
                with col1:
                    st.write(f"Course: {course}")
                with col2:
                    if course in st.session_state.xpath_values:
                        st.text_area("XPath", value=st.session_state.xpath_values[course], 
                                   key=f"xpath_view_{i}", disabled=True)
                with col3:
                    if st.button("Remove", key=f"remove_xpath_{i}"):
                        courses_to_remove.append(course)

            if courses_to_remove:
                for course in courses_to_remove:
                    if course in st.session_state.courses:
                        st.session_state.courses.remove(course)
                    if course in st.session_state.xpath_values:
                        del st.session_state.xpath_values[course]
                st.rerun()

            if st.button("Generate Url YAML"):
                xpath_content = generate_xpath_yaml(courses=st.session_state.courses)
                st.download_button(
                    label="Download Url YAML",
                    data=xpath_content,
                    file_name="course_url.yaml",
                    mime="text/yaml"
                )

    # Reset button
    if st.session_state.active_section:
        if st.button("Reset All"):
            st.session_state.courses = []
            st.session_state.schedule = {
                'Monday': [], 'Tuesday': [], 'Wednesday': [],
                'Thursday': [], 'Friday': []
            }
            st.session_state.active_section = None
            st.session_state.xpath_values = {}
            st.rerun()

if __name__ == "__main__":
    main()