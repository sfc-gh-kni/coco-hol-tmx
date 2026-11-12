import streamlit as st

from components import ctx

c = ctx()

st.title("Meet CoCo")
st.markdown(
    "**Cortex Code (CoCo)** is Snowflake's AI coding agent, built into Snowsight. In this lab you use it from the **side panel** in Workspaces. Five minutes here saves twenty later."
)

st.markdown("#### What CoCo can do here")
with st.container(horizontal=True):
    for icon, title, body in [
        ("ac_unit", "Create", "Create objects you ask for, such as your Iceberg table or a view, after you approve the statement."),
        ("travel_explore", "Explore", "Find tables, read their columns and profile the data with read-only queries."),
        ("code", "Write SQL", "Draft, explain, fix and validate SQL, writing it into your open file."),
        ("web", "Build apps", "Create and edit Streamlit app files in your workspace."),
        ("description", "Report", "Turn a query into a self-contained HTML report."),
    ]:
        with st.container(border=True, height="stretch"):
            st.markdown(f":material/{icon}: **{title}**")
            st.caption(body)

st.markdown("#### What CoCo can't do")
st.markdown(
    f"""
- **Go beyond your role.** CoCo acts as you, with `{c['role']}`. If you can't read or change something, neither can it. The Marketplace view is read-only for everyone.
- **Act without you.** With approvals on, every SQL statement and file change waits for your OK.
- **See other chats.** Each conversation starts fresh. Within one conversation it remembers earlier turns, and it also sees the file that's open beside it.
- **Guarantee the same output twice.** Wording, SQL style and app layout vary between runs and between people. The **numbers** shouldn't.
"""
)

st.markdown("#### The four things CoCo will ask you")
st.table(
    [
        {"You'll see": "A SQL statement with approve / reject", "What it means": "CoCo wants to run a query", "What to do": "Read it. Approve only reads, unless the step says otherwise (exercise 1 creates your table)."},
        {"You'll see": "A highlighted change with **Undo / Keep**", "What it means": "CoCo edited a file", "What to do": "Skim the change, then Keep or Undo."},
        {"You'll see": "A plan ending *Proceed, modify, or cancel?*", "What it means": "A multi-step task is about to start", "What to do": "Check the scope, then reply `Proceed`."},
        {"You'll see": "Scoping questions", "What it means": "A skill wants more detail", "What to do": "In this lab, cancel them. The prompts already contain the answers."},
    ],
    hide_index=True,
)
st.caption("If CoCo seems stuck, it's almost always waiting for one of these.")

st.markdown("#### Anatomy of a good prompt")
st.markdown("Every prompt in this guide follows the same pattern. Here's prompt 3.1, split into its parts:")

ANATOMY = [
    ("Goal", "blue", "Write a read-only query that pivots … to one row per ticker and date"),
    ("Objects", "violet", c["prices"]),
    ("Scope", "orange", "for the exchange operators NDAQ, ICE, CME and CBOE from 2026-04-01 to 2026-06-30"),
    ("Output", "green", "summarize per ticker: trading days, distinct dates, missing closes, average Nasdaq volume, and min/max close"),
    ("Guardrails", "red", "read-only … use fully qualified names and show the SQL before running it"),
]
with st.container(border=True):
    for label, color, text in ANATOMY:
        st.markdown(f":{color}-badge[{label}] {text}")

st.markdown(
    """
- **Goal:** the outcome, in one sentence.
- **Objects:** fully qualified names, so CoCo doesn't guess.
- **Scope:** filters, dates and entities.
- **Output:** the exact columns or artifact you want, so the result is checkable.
- **Guardrails:** what CoCo must and mustn't do (read-only, no packages, don't deploy, don't publish).
"""
)

st.markdown("#### Follow-ups that work well")
st.code(
    """Explain this query line by line.
Why is your result different from <expected>? Show the query you used.
Prove there are no duplicate rows at the ticker and date grain.
Rewrite this with a CTE so it's easier to read.
What assumptions did you make? List them.""",
    language="text",
)

st.info(
    "Write prompts the way you'd brief a sharp new analyst: specific about the goal and the data, explicit about the boundaries. CoCo can do most of the work; you're responsible for checking it.",
    icon=":material/lightbulb:",
)
