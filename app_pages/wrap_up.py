import streamlit as st

from components import APP_SCHEMA, completed_prompt_count, total_prompt_count

st.title("Wrap-up and Q&A")
st.markdown(":material/schedule: **1:40–2:00 (20 min)**")

done, total = completed_prompt_count(), total_prompt_count()
if done == total:
    st.success("You completed every prompt and step. Nice work.", icon=":material/celebration:")
else:
    st.info(f"You've ticked {done} of {total} prompts and steps. Anything left over is fine to finish later.", icon=":material/info:")

st.markdown("#### What you built")
st.markdown(
    f"""
- A data profile of the lab tables, with freshness and caveats checked.
- Reviewed, validated SQL: a pivot, a summary and a correctness check.
- Window-function analysis of 2026 returns and the largest daily moves.
- A **deployed Streamlit app** in `{APP_SCHEMA}`.
- A private HTML report built from a query.
"""
)

st.markdown("#### The habits that carry over")
st.markdown(
    """
1. **Ground CoCo in real objects.** Use fully qualified names and say *read-only* when you mean it.
2. **Review before you approve.** Read SQL, plans and file changes before you accept them.
3. **Verify, don't trust.** Check grain, date windows and edge cases with a second query.
4. **Know your data's limits.** Adjusted vs raw prices, venue vs total volume, lagged vs live data.
"""
)

st.markdown("#### Q&A prompts")
st.markdown(
    """
- Where could CoCo save you time in your own work this month?
- What would you need to check before using an app like this on real data?
- What surprised you about CoCo's plans or approvals?
"""
)

st.markdown("#### After the session")
st.markdown(
    """
- Leave your app and files in place. The facilitator's team cleans up the lab objects afterwards.
- Lab access and the shared role may be removed after the workshop, so save anything you want to keep, such as prompts or code you wrote. **Don't** copy data out of the account.
"""
)

st.markdown("#### Learn more")
with st.container(horizontal=True):
    st.link_button("CoCo in Snowsight", "https://docs.snowflake.com/en/user-guide/cortex-code/cortex-code-snowsight", icon=":material/open_in_new:")
    st.link_button("Streamlit in Workspaces", "https://docs.snowflake.com/en/developer-guide/streamlit/streamlit-in-workspaces/streamlit-in-workspaces-create-run", icon=":material/open_in_new:")
    st.link_button("HTML reports", "https://docs.snowflake.com/en/user-guide/ui-snowsight/reports", icon=":material/open_in_new:")
    st.link_button("Stock data source", "https://data-docs.snowflake.com/sources/stocks", icon=":material/open_in_new:")
