import streamlit as st
import yaml
from utils import validate_time_format, generate_course_schedule_yaml, generate_url_yaml

def main():
    st.set_page_config(page_title="Course Schedule YAML Generator", layout="wide")
    st.title("Course Schedule YAML Generator")
    st.markdown("""
    Generate YAML files for course schedules and URL mappings.
    Choose an option below to get started.
    """)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Create Course Schedule YAML", use_container_width=True):
            st.session_state.active_section = "schedule"
    with col2:
        if st.button("Create Course URL YAML", use_container_width=True):
            st.session_state.active_section = "url"
    if 'courses' not in st.session_state:
        st.session_state.courses = []
    if 'schedule' not in st.session_state:
        st.session_state.schedule = {'Monday': [], 'Tuesday': [], 'Wednesday': [], 'Thursday': [], 'Friday': []}
    if 'active_section' not in st.session_state:
        st.session_state.active_section = None
    if 'url_values' not in st.session_state:
        st.session_state.url_values = {}
    if st.session_state.active_section == "schedule":
        st.header("Course Schedule Generator")
        with st.container():
            st.subheader("Add New Course")
            with st.form("course_form"):
                day = st.selectbox("Select Day", ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'])
                course_name = st.text_input("Course Name *")
                col1, col2 = st.columns(2)
                with col1:
                    start_time = st.text_input("Start Time (HH:MM) *", placeholder="12:05")
                with col2:
                    end_time = st.text_input("End Time (HH:MM) *", placeholder="13:05")
                send_message = st.selectbox("Send Message", options=[False, True], index=0)
                if st.form_submit_button("Add Course"):
                    if not all([course_name, start_time, end_time]):
                        st.error("Please fill in all fields")
                    else:
                        valid_start = validate_time_format(start_time)
                        valid_end = validate_time_format(end_time)
                        if not valid_start or not valid_end:
                            st.error("Invalid time format. Use HH:MM format (e.g., 12:05)")
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
        if any(courses for courses in st.session_state.schedule.values()):
            if st.button("Generate Schedule YAML"):
                yaml_content = generate_course_schedule_yaml(st.session_state.schedule)
                st.download_button(label="Download Schedule YAML", data=yaml_content, file_name="course_details.yaml", mime="text/yaml")
    elif st.session_state.active_section == "url":
        st.header("Course URL Generator")
        with st.form("url_form"):
            if not st.session_state.courses:
                st.warning("Please add courses in the Course Schedule section first.")
                course_name = st.text_input("Course Name", disabled=True)
                url_value = st.text_area("Course URL", disabled=True)
                st.form_submit_button("Add Course", disabled=True)
            else:
                course_name = st.selectbox("Select Course", options=st.session_state.courses)
                url_value = st.text_area("Course URL", placeholder="https://example.com/course")
                if st.form_submit_button("Add Course"):
                    if not url_value:
                        st.error("Please enter the Course URL")
                    else:
                        st.session_state.url_values[course_name] = url_value
                        st.success(f"Added URL for {course_name}")
        if st.button("Generate URL YAML"):
            url_content = generate_url_yaml(st.session_state.url_values)
            st.download_button(label="Download URL YAML", data=url_content, file_name="course_url.yaml", mime="text/yaml")
if __name__ == "__main__":
    main()
