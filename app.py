import streamlit as st
import yaml
from utils import validate_time_format, generate_course_schedule_yaml, generate_url_yaml, validate_url

def main():
    st.set_page_config(page_title="Course Schedule YAML Generator", layout="wide")

    st.title("Course Schedule YAML Generator")
    st.markdown("""
    Generate YAML files for course schedules and course URLs.
    Choose an option below to get started.
    """)

    # Two columns for the main buttons
    col1, col2 = st.columns(2)

    with col1:
        if st.button("Create Course Schedule YAML", use_container_width=True):
            st.session_state.active_section = "schedule"

    with col2:
        if st.button("Create URL Course YAML", use_container_width=True):
            st.session_state.active_section = "url"

    # Initialize session state
    if 'courses' not in st.session_state:
        st.session_state.courses = []
    if 'schedule' not in st.session_state:
        st.session_state.schedule = {
            'Monday': [], 'Tuesday': [], 'Wednesday': [],
            'Thursday': [], 'Friday': []
        }
    if 'active_section' not in st.session_state:
        st.session_state.active_section = None
    if 'url_values' not in st.session_state:
        st.session_state.url_values = {}

    # Course Schedule YAML Section
    if st.session_state.active_section == "schedule":
        st.header("Course Schedule Generator")

        # Course input form
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

        # Display current schedule
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
                                st.session_state.schedule[day].pop(idx)

                                # Check if course exists in other days
                                is_used = False
                                for other_day, courses in st.session_state.schedule.items():
                                    if any(c['name'] == course_name for c in courses):
                                        is_used = True
                                        break

                                if not is_used:
                                    if course_name in st.session_state.courses:
                                        st.session_state.courses.remove(course_name)
                                    if course_name in st.session_state.url_values:
                                        del st.session_state.url_values[course_name]
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

    # URL YAML Section
    elif st.session_state.active_section == "url":
        st.header("Course URL Generator")
        st.info("Note: Course names must match exactly with those used in the course schedule YAML file.")

        with st.form("url_form"):
            if not st.session_state.courses:
                st.warning("Please add courses in the Course Schedule section first.")
                course_name = st.text_input("Course Name", disabled=True)
                url_value = st.text_input("Course URL", disabled=True)
                st.form_submit_button("Add Course", disabled=True)
            else:
                course_name = st.selectbox(
                    "Select Course",
                    options=st.session_state.courses,
                    help="Select from courses already added to the schedule"
                )
                url_value = st.text_input("Course URL", 
                                     placeholder="https://example.com/course",
                                     help="Enter the complete URL for the course")

                if st.form_submit_button("Add Course"):
                    if not url_value:
                        st.error("Please enter the URL")
                    elif not validate_url(url_value):
                        st.error("Please enter a valid URL (e.g., https://example.com/course)")
                    else:
                        st.session_state.url_values[course_name] = url_value
                        st.success(f"Added URL for {course_name}")

        if st.session_state.courses:
            st.subheader("Current Courses")
            courses_to_remove = []
            for i, course in enumerate(st.session_state.courses):
                col1, col2, col3 = st.columns([2, 2, 1])
                with col1:
                    st.write(f"Course: {course}")
                with col2:
                    if course in st.session_state.url_values:
                        st.text_input("URL", value=st.session_state.url_values[course], 
                                   key=f"url_view_{i}", disabled=True)
                with col3:
                    if st.button("Remove", key=f"remove_url_{i}"):
                        courses_to_remove.append(course)

            if courses_to_remove:
                for course in courses_to_remove:
                    # Only remove the URL mapping, keep the course in the schedule
                    if course in st.session_state.url_values:
                        del st.session_state.url_values[course]
                st.rerun()

            if st.button("Generate URL YAML"):
                url_content = generate_url_yaml(courses=st.session_state.courses)
                st.download_button(
                    label="Download URL YAML",
                    data=url_content,
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
            st.session_state.url_values = {}
            st.rerun()

if __name__ == "__main__":
    main()