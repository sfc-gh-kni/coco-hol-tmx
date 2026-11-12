import re

import streamlit as st

PREFIX = "DEV_EDX_HACKATHONTOR"
S3_PREFIX = "DEV_HACKATHONTOR"
SCHEMA = "CONSUMER"
SOURCE_VIEW = "SNOWFLAKE_CURATED_DATA_FREE.PUBLIC_DATA_FREE.STOCK_PRICE_TIMESERIES"
EXCHANGE_OPERATORS = ["NDAQ", "ICE", "CME", "CBOE"]
BENCHMARK_ETFS = ["SPY", "QQQ", "EWC"]
CANADIAN_INTERLISTED = ["RY", "TD", "BMO", "BNS", "ENB", "CNQ", "SHOP"]

TEAMS = [
    "AGENTARCHITECTS",
    "BYTEBANDITS",
    "CLOUDCRAFTERS",
    "DATADRAGONS",
    "ICEBERGINNOVATORS",
    "LOGICLEGENDS",
    "MODELMAVERICKS",
    "NEURALNINJAS",
    "PIXELPIONEERS",
    "PROMPTPREDATORS",
    "QUERYQUEST",
    "ROCKETROCKSTARS",
    "SCHEMASHIFTERS",
    "VPCVOYAGERS",
    "WAREHOUSEWARRIOR",
]

EXERCISE_PROMPTS = {
    0: ["0.1", "0.2"],
    1: ["1.1", "1.2"],
    2: ["2.1"],
    3: ["3.1", "3.2"],
    4: ["4.1"],
    5: ["5.1", "5.2", "5.3"],
    6: ["6.1"],
}

_INITIALS_RE = re.compile(r"^[A-Z][A-Z0-9]{1,5}$")


def clean_initials(raw: str) -> str:
    return re.sub(r"[^A-Z0-9]", "", (raw or "").upper())


def team_names(team: str) -> dict:
    return {
        "Role": f"{PREFIX}_{team}_ANALYST_OKTA",
        "Functional role": f"{PREFIX}_{team}_ANALYST_FR",
        "Warehouse": f"{PREFIX}_{team}_USER_WH",
        "Database": f"{PREFIX}_{team}_DB",
        "Schema": SCHEMA,
        "External volume": f"{S3_PREFIX}_{team}_S3_EXT_VOL",
    }


def ctx() -> dict:
    """The attendee's object names. Placeholders until team and initials are set in the sidebar."""
    team = st.session_state.get("team_w") or "<TEAM>"
    initials = clean_initials(st.session_state.get("initials_w", ""))
    ok_initials = bool(_INITIALS_RE.match(initials))
    initials = initials if ok_initials else "<INITIALS>"
    names = team_names(team)
    database = names["Database"]
    return {
        "team": team,
        "initials": initials,
        "ready": team in TEAMS and ok_initials,
        "role": names["Role"],
        "fr_role": names["Functional role"],
        "warehouse": names["Warehouse"],
        "database": database,
        "schema": f"{database}.{SCHEMA}",
        "ext_vol": names["External volume"],
        "table": f"STOCK_PRICE_TIMESERIES_{initials}",
        "prices": f"{database}.{SCHEMA}.STOCK_PRICE_TIMESERIES_{initials}",
    }


def render_context_picker():
    """Sidebar team and initials inputs. Kept in session state and the URL so a refresh doesn't lose them."""
    qp = st.query_params
    if "_team_default" not in st.session_state:
        st.session_state["_team_default"] = TEAMS.index(qp["team"]) if qp.get("team") in TEAMS else None
        st.session_state["_initials_default"] = clean_initials(qp.get("initials", ""))
    st.selectbox(
        "Your team",
        TEAMS,
        index=st.session_state["_team_default"],
        key="team_w",
        placeholder="Pick your team",
    )
    st.text_input(
        "Your initials",
        value=st.session_state["_initials_default"],
        key="initials_w",
        max_chars=6,
        placeholder="For example KN",
        help="2–6 letters or digits, starting with a letter. They become the suffix of your table, view and app names.",
    )
    raw = st.session_state.get("initials_w", "")
    if raw and not _INITIALS_RE.match(clean_initials(raw)):
        st.error("Use 2–6 letters or digits, starting with a letter.", icon=":material/error:")
    c = ctx()
    if c["ready"]:
        st.query_params["team"] = c["team"]
        st.query_params["initials"] = c["initials"]
        st.caption(f"Names in this guide are filled in for **{c['team']}** and **{c['initials']}**.")
    else:
        st.caption("Pick your team and enter your initials: every prompt and SQL block fills in your names.")


def require_context():
    if not ctx()["ready"]:
        st.warning(
            "Pick **your team** and enter **your initials** in the sidebar first. Until then, prompts show `<TEAM>` and `<INITIALS>` placeholders.",
            icon=":material/badge:",
        )


def _done_store() -> dict:
    if "_done" not in st.session_state:
        st.session_state["_done"] = {}
    return st.session_state["_done"]


def _key(prompt_id: str) -> str:
    return prompt_id.replace(".", "_")


def _on_toggle(prompt_id: str):
    key = _key(prompt_id)
    _done_store()[key] = st.session_state[f"_cb_{key}"]


def is_exercise_complete(exercise: int) -> bool:
    prompts = EXERCISE_PROMPTS.get(exercise, [])
    store = _done_store()
    return bool(prompts) and all(store.get(_key(p), False) for p in prompts)


def completed_prompt_count() -> int:
    store = _done_store()
    return sum(
        store.get(_key(p), False) for ps in EXERCISE_PROMPTS.values() for p in ps
    )


def total_prompt_count() -> int:
    return sum(len(ps) for ps in EXERCISE_PROMPTS.values())


def render_header(exercise: int, title: str, time_range: str, goal: str):
    st.title(f"{exercise}. {title}" if exercise else title)
    with st.container(horizontal=True, gap="large"):
        st.markdown(f":material/schedule: **{time_range}**", width="content")
        st.markdown(f":material/flag: **Goal:** {goal}", width="content")
    st.space("small")


def render_prompt(prompt_id: str, title: str, prompt_text: str, optional: bool = False):
    """A copyable prompt card. Optional prompts don't count toward core progress."""
    key = _key(prompt_id)
    cb_key = f"_cb_{key}"
    if cb_key not in st.session_state:
        st.session_state[cb_key] = _done_store().get(key, False)
    badge = " :gray-badge[Optional]" if optional else ""
    with st.container(border=True):
        title_col, done_col = st.columns([6, 1], vertical_alignment="center")
        title_col.markdown(f"#### :material/terminal: Prompt {prompt_id}: {title}{badge}")
        done_col.checkbox(
            "Done", key=cb_key, on_change=_on_toggle, args=(prompt_id,)
        )
        st.caption(
            "Copy with the icon in the top-right corner of the box, then paste "
            "into the CoCo side panel."
        )
        st.code(prompt_text, language="text", wrap_lines=True)


def render_checkpoint(step_id: str, title: str, body: str):
    """A tracked step that is done in the Snowsight UI rather than pasted into CoCo."""
    key = _key(step_id)
    cb_key = f"_cb_{key}"
    if cb_key not in st.session_state:
        st.session_state[cb_key] = _done_store().get(key, False)
    with st.container(border=True):
        title_col, done_col = st.columns([6, 1], vertical_alignment="center")
        title_col.markdown(f"#### :material/touch_app: Step {step_id}: {title}")
        done_col.checkbox(
            "Done", key=cb_key, on_change=_on_toggle, args=(step_id,)
        )
        st.markdown(body)


def render_check(body: str, title: str = "Check your result"):
    with st.expander(f":material/fact_check: {title}"):
        st.markdown(body)


def render_learn(title: str, body: str):
    with st.expander(f":material/school: {title}"):
        st.markdown(body)


def render_tools(tools: list[dict]):
    """Cards naming the Snowflake features an exercise uses: name, description, icon."""
    st.markdown("##### :material/build: Tools in this exercise")
    cols = st.columns(len(tools))
    for col, tool in zip(cols, tools):
        with col.container(border=True, height="stretch"):
            st.markdown(f":material/{tool.get('icon', 'widgets')}: **{tool['name']}**")
            st.caption(tool["description"])
    st.space("small")


def render_review(items: list[str], title: str = "Before you approve"):
    """Checklist for reviewing what CoCo proposes before accepting it."""
    with st.container(border=True):
        st.markdown(f"##### :material/rule: {title}")
        st.markdown("\n".join(f"- {item}" for item in items))


def render_go_further(note: str = "Only if you're ahead of the agenda. These don't count toward your progress."):
    st.markdown("#### :material/explore: Go further")
    st.caption(note)


def render_key_concepts(concepts: list[tuple[str, str]]):
    st.markdown("##### :material/lightbulb: Key concepts")
    for term, definition in concepts:
        with st.expander(f"**{term}**"):
            st.markdown(definition)


def render_takeaways(items: list[str]):
    st.markdown("##### :material/check_circle: What you just did")
    st.markdown("\n".join(f"- {item}" for item in items))
