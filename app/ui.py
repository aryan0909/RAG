import streamlit as st

from app.rag import answer_question


st.set_page_config(
    page_title="Company Policy Assistant",
    page_icon="💬",
    layout="centered",
)

st.title("💬 Company Policy Assistant")
st.caption("Ask questions about company policies. Answers are based on retrieved documents.")

# Keep the conversation in Streamlit's session state.
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display the existing conversation.
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

        # Show retrieved sources for assistant responses.
        if message["role"] == "assistant" and message.get("sources"):
            with st.expander("View sources"):
                for source in message["sources"]:
                    st.markdown(
                        f"**{source['source']} — Chunk {source['chunk_id']}**"
                    )
                    st.caption(
                        f"Distance: {source['distance']:.4f}"
                    )
                    st.write(source["text"])

# Display the chat input.
if question := st.chat_input("Ask a company policy question..."):
    # Show and save the user's question.
    st.session_state.messages.append(
        {"role": "user", "content": question}
    )

    with st.chat_message("user"):
        st.markdown(question)

    # Retrieve context and generate the answer.
    with st.chat_message("assistant"):
        with st.spinner("Searching documents and generating an answer..."):
            try:
                result = answer_question(question)
                answer = result["answer"]
                sources = result["sources"]

            except Exception:
                st.error(
                    "Something went wrong while processing your question. "
                    "Check that Ollama is running and try again."
                )
                st.stop()

        st.markdown(answer)

        if sources:
            with st.expander("View sources"):
                for source in sources:
                    st.markdown(
                        f"**{source['source']} — Chunk {source['chunk_id']}**"
                    )
                    st.caption(
                        f"Distance: {source['distance']:.4f}"
                    )
                    st.write(source["text"])

    # Save the answer and sources for future rerenders.
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer,
            "sources": sources,
        }
    )
