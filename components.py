import streamlit as st

ROLE = "TMX_HOL_ATTENDEE"
WAREHOUSE = "TMX_HOL_WH"
APP_SCHEMA = "TMX_COCO_HOL.LAB"
PRICES = "TMX_COCO_HOL.SOURCE.STOCK_PRICE_TIMESERIES"
WATCHLIST = "TMX_COCO_HOL.SOURCE.WATCHLIST"

EXERCISE_PROMPTS = {
    0: ["0.1"],
    1: ["1.1"],
    2: ["2.1", "2.2"],
    3: ["3.1"],
    4: ["4.1", "4.2", "4.3"],
    5: ["5.1"],
}


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
