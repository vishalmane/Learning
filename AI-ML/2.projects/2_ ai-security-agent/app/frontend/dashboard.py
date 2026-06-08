"""Streamlit dashboard for security operators."""

from threading import Event, Thread

import streamlit as st

from app.vision.camera_service import preview_camera


def initialize_state() -> None:
    """Initialize Streamlit session state for camera preview controls."""
    if "camera_on" not in st.session_state:
        st.session_state.camera_on = False
    if "camera_stop_event" not in st.session_state:
        st.session_state.camera_stop_event = None
    if "camera_thread" not in st.session_state:
        st.session_state.camera_thread = None


def start_preview() -> None:
    """Start the OpenCV camera preview window."""
    thread = st.session_state.camera_thread
    if thread is not None and thread.is_alive():
        return

    stop_event = Event()
    st.session_state.camera_stop_event = stop_event
    st.session_state.camera_thread = Thread(
        target=preview_camera,
        args=(stop_event,),
        daemon=True,
    )
    st.session_state.camera_thread.start()
    st.session_state.camera_on = True


def stop_preview() -> None:
    """Stop the OpenCV camera preview window."""
    stop_event = st.session_state.camera_stop_event
    if stop_event is not None:
        stop_event.set()

    thread = st.session_state.camera_thread
    if thread is not None and thread.is_alive():
        thread.join(timeout=2)

    st.session_state.camera_thread = None
    st.session_state.camera_stop_event = None
    st.session_state.camera_on = False


def main() -> None:
    """Render the operator dashboard with camera preview controls."""
    st.set_page_config(page_title="AI Security Agent", layout="wide")
    initialize_state()

    st.title("AI Security Agent")

    control_columns = st.columns([1, 1, 5])
    with control_columns[0]:
        if st.button("Start", use_container_width=True, disabled=st.session_state.camera_on):
            start_preview()
    with control_columns[1]:
        if st.button("Stop", use_container_width=True, disabled=not st.session_state.camera_on):
            stop_preview()

    if st.session_state.camera_on:
        st.success("Camera preview window is open.")
    else:
        st.info("Camera preview is off.")


if __name__ == "__main__":
    main()
