import streamlit as st

from questions.Question import Question


class QuestionDrawer:
    """Public class for displaying questions."""

    @staticmethod
    def evaluateAnswer(current_question: Question, user_input: any) -> None:
        """Evaluate the answer after submitting it."""
        if (user_input is not None) or (user_input == 0):
            is_correct, feedback = current_question.verifyAndFeedback(user_input)
            if is_correct:
                st.markdown(
                    "<span style='color: green;'>Your answer is correct!</span>",
                    unsafe_allow_html=True,
                )
                st.markdown(
                    f"<span style='color: green;'>{feedback}</span>",
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    "<span style='color: red;'>Your answer is incorrect!</span>",
                    unsafe_allow_html=True,
                )
                st.markdown(
                    f"<span style='color: red;'>{feedback}</span>",
                    unsafe_allow_html=True,
                )

    @staticmethod
    def drawQuestion(current_question: Question) -> None:
        """Draw the selected question."""
        st.title(current_question.title)
        current_question.drawImage()
        st.text(current_question.bodytext)

        user_input = current_question.drawYourself()

        if st.button("Submit Answer", key=f"submit_button_{current_question.name}"):
            QuestionDrawer.evaluateAnswer(current_question, user_input)

        if st.button("Reset", key=f"reset_button_{current_question.name}"):
            st.session_state[current_question.widget_key] = current_question.default
            st.rerun()
