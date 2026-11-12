from pathlib import Path

import streamlit as st

from components import completed_prompt_count, is_exercise_complete, total_prompt_count

_DIR = Path(__file__).parent


def _title(exercise: int, label: str) -> str:
    check = " :green[:material/check_circle:]" if is_exercise_complete(exercise) else ""
    return f"{exercise}. {label}{check}"


st.set_page_config(
    page_title="TMX CoCo hands-on lab",
    page_icon=":material/candlestick_chart:",
    layout="wide",
)

st.logo(
    str(_DIR / "static" / "snowflake_full_logo.png"),
    icon_image=str(_DIR / "static" / "snowflake_logo.png"),
)

page = st.navigation(
    {
        "": [
            st.Page("app_pages/home.py", title="Home", icon=":material/home:", default=True),
            st.Page(
                "app_pages/getting_started.py",
                title=f"Get started{' :green[:material/check_circle:]' if is_exercise_complete(0) else ''}",
                icon=":material/rocket_launch:",
            ),
        ],
        "Hands-on (90 min)": [
            st.Page("app_pages/ex1_discover.py", title=_title(1, "Discover the data"), icon=":material/travel_explore:"),
            st.Page("app_pages/ex2_sql.py", title=_title(2, "Generate and validate SQL"), icon=":material/database:"),
            st.Page("app_pages/ex3_trends.py", title=_title(3, "Compare trends"), icon=":material/trending_up:"),
            st.Page("app_pages/ex4_streamlit.py", title=_title(4, "Build and deploy an app"), icon=":material/web:"),
            st.Page("app_pages/ex5_report.py", title=_title(5, "HTML report snapshot"), icon=":material/description:"),
        ],
        "Help": [
            st.Page("app_pages/troubleshooting.py", title="Troubleshooting", icon=":material/build:"),
            st.Page("app_pages/wrap_up.py", title="Wrap-up and Q&A", icon=":material/forum:"),
        ],
    },
    position="sidebar",
)

with st.sidebar:
    done, total = completed_prompt_count(), total_prompt_count()
    st.progress(done / total, text=f"{done} of {total} done")
    st.caption("Progress is kept in this browser tab only.")

page.run()
