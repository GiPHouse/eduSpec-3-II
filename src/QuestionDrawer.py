import streamlit as st

from Question import Question


class QuestionDrawer:
    """Public class for displaying questions"""

    @staticmethod
    def drawQuestion(current_question: Question) -> None:
        """draws the parts of the question that are the same for all questions

        Args:
            current_question (Question): _description_
        """
        with st.container():
            st.title(current_question.title)
            if current_question.imgpath:
                st.image(current_question.imgpath)
            st.text(current_question.bodytext)
            st.title("this is a test")

            # depending on question we have an input field or smth
            user_input = current_question.drawYourself()
            if st.button("Submit Answer", key="submit button"):
                feedback = current_question.verifyAndFeedback(user_input)
                st.write(feedback)

            # if st.button("Reset"):
            #     st.rerun()
