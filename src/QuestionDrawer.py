import streamlit as st

from Question import Question


class QuestionDrawer:
    """QuestionDrawer."""

    @staticmethod
    def drawQuestion(current_question: Question) -> None:
        """_summary_

        Args:
            current_question (Question): the question to be drawn
        """
        st.title(current_question.title)
        st.text(current_question.bodytext)

        if getattr(current_question, "imgpath", None):
            st.image(current_question.imgpath, width="stretch")

        user_input = current_question.drawYourself()
        if st.button("Submit Answer", key="submit_button"):
            is_correct, feedback = current_question.verifyAndFeedback(user_input)
            if is_correct:
                st.markdown(
                    "<span style='color: green;'>Your answer is correct!</span>",
                    unsafe_allow_html=True,
                )
                st.markdown(
                    f"<span style='color: green;'>{feedback}</span>", unsafe_allow_html=True
                )
            else:
                st.markdown(
                    "<span style='color: red;'>Your answer is incorrect!</span>",
                    unsafe_allow_html=True,
                )
                st.markdown(f"<span style='color: red;'>{feedback}</span>", unsafe_allow_html=True)
