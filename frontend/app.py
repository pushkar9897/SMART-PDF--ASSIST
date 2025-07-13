import streamlit as st, requests

API = "http://localhost:8000"
st.set_page_config(page_title="Smart Research Assistant")
st.title("📄 Smart PDF Assist")

if "doc_id" not in st.session_state:
    st.session_state["doc_id"] = None
if "history" not in st.session_state:
    st.session_state["history"] = []

uploaded = st.file_uploader("Upload PDF or TXT", type=["pdf", "txt"])
if uploaded and st.session_state["doc_id"] is None:
    r = requests.post(f"{API}/upload", files={"file": uploaded})
    if r.ok:
        res = r.json()
        st.session_state["doc_id"] = res.get("document_id")
        st.success("Summary: " + res["summary"])

if st.session_state["doc_id"]:
    mode = st.radio("Mode", ["Ask Anything", "Challenge Me"])

    if mode == "Ask Anything":
        with st.form("ask_form"):
            q = st.text_input("Ask a question")
            send = st.form_submit_button("Send")
            if send and q:
                r = requests.post(f"{API}/ask", json={
                    "document_id": st.session_state["doc_id"],
                    "question": q,
                    "conversation_history": st.session_state["history"],
                })
                if r.ok:
                    ans = r.json()
                    st.write("**Answer:**", ans["answer"])
                    st.write("**Justification:**", ans["justification"])
                    st.code(ans["snippet"])
                    # Store as dict for backend compatibility
                    st.session_state["history"].append({
                        "question": q,
                        "answer": ans["answer"],
                        "justification": ans.get("justification", "")
                    })

    else:  # Challenge Me
        if "challenges" not in st.session_state:
            r = requests.get(f"{API}/challenges", params={"document_id": st.session_state["doc_id"]})
            st.session_state["challenges"] = r.json()
        for i, ch in enumerate(st.session_state["challenges"]):
            with st.expander(f"Challenge {i+1}"):
                st.write(ch["question"])
                user = st.text_area("Your answer", key=f"u{i}")
                if st.button("Submit", key=f"s{i}"):
                    r = requests.post(f"{API}/evaluate", json={
                        "document_id": st.session_state["doc_id"],
                        "challenge_index": i,
                        "user_answer": user,
                    })
                    st.json(r.json())