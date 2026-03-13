import streamlit as st

from questions.Question import Question


class QuestionDrawer:
    """Public class for displaying questions"""

    def evaluateAnswer(current_question: Question, user_input: any) -> None:
        """Evaluates the answer after submitting it

        Args:
            current_question (Question): The question that is aimed to be displayed
            user_input (_type_): user's answer to the question
        """
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
        """Draws the parts of the question that are the same for all questions

        Args:
            current_question (Question): The question that is aimed to be displayed
        """
        with st.container():
            st.title(current_question.title)
            current_question.drawImage()
            st.text(current_question.bodytext)

            with st.form("form" + current_question.title, enter_to_submit=False):
                user_input = current_question.drawYourself()
                if st.form_submit_button("Submit Answer", key="submit_button_form"):
                    if user_input is not None:
                        QuestionDrawer.evaluateAnswer(current_question, user_input)

            def _reset_callback() -> None:
                st.session_state[current_question.widget_key] = current_question.default

            if st.button("Reset", on_click=_reset_callback):
                st.rerun()
