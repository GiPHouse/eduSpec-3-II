import streamlit as st

from QuestionDrawer import QuestionDrawer
from questions.Question import Question


class Quiz:
    """Class to create the elements of a quiz including handling of answer tracking."""

    def __init__(self, name: str, question_list: list[Question]) -> None:
        """Initialises a quiz instance.

        Args:
            name (str): The unique name/id of the quiz.
            question_list (list[Question]): A list of questions in the quiz.
        """
        self.name = name
        if "current_index" not in st.session_state:
            st.session_state["current_index"] = 0
        self.current_index = 0
        self.question_list = question_list
        # Use quiz name in the key so each quiz has its own index
        if f"current_index_{self.name}" not in st.session_state:
            st.session_state[f"current_index_{self.name}"] = 0
        self.current_index = st.session_state[f"current_index_{self.name}"]

        # Track answers: {question_index: {"correct": bool, "title": str}}
        if f"answers_{self.name}" not in st.session_state:
            st.session_state[f"answers_{self.name}"] = {}

        # Track attempts per question: {question_index: number_of_attempts}
        if f"attempts_{self.name}" not in st.session_state:
            st.session_state[f"attempts_{self.name}"] = {}

        # Track if overview is being shown
        if f"show_overview_{self.name}" not in st.session_state:
            st.session_state[f"show_overview_{self.name}"] = False

        # Track if quiz is completed
        if f"quiz_completed_{self.name}" not in st.session_state:
            st.session_state[f"quiz_completed_{self.name}"] = False

    def recordAnswer(self, question_index: int, is_correct: bool) -> None:
        """Records whether a question was answered correctly and tracks attempts.

        Args:
            question_index (int): The index of the question.
            is_correct (bool): Whether the answer was correct.
        """
        question = self.question_list[question_index]
        
        # Increment attempt count
        attempts_key = f"attempts_{self.name}"
        if question_index not in st.session_state[attempts_key]:
            st.session_state[attempts_key][question_index] = 0
        st.session_state[attempts_key][question_index] += 1
        
        # Record answer (only update to correct if they got it right)
        answers_key = f"answers_{self.name}"
        current_answer = st.session_state[answers_key].get(question_index, {})
        
        # If already marked correct, don't change it
        if current_answer.get("correct", False):
            return
        
        st.session_state[answers_key][question_index] = {
            "correct": is_correct,
            "title": question.title,
        }

    def isQuizComplete(self) -> bool:
        """Checks if all questions have been answered."""
        answers = st.session_state[f"answers_{self.name}"]
        return len(answers) == len(self.question_list)

    def drawReviewPage(self) -> None:
        """Draws the final review page showing results."""
        answers = st.session_state[f"answers_{self.name}"]

        # Show balloons on first view of review page
        if not st.session_state.get(f"balloons_shown_{self.name}", False):
            st.balloons()
            st.session_state[f"balloons_shown_{self.name}"] = True

        st.title("Quiz Complete! 🎉")

        # Calculate score
        correct_count = sum(1 for a in answers.values() if a["correct"])
        total = len(self.question_list)

        st.metric("Your Score", f"{correct_count} / {total}")

        # Show incorrect questions
        wrong_questions = [
            (idx, data) for idx, data in answers.items() if not data["correct"]
        ]

        if wrong_questions:
            st.subheader("Questions to Review")
            for idx, data in wrong_questions:
                with st.expander(f"❌ Question {idx + 1}: {data['title']}"):
                    st.write(f"Go back and review this question.")
                    if st.button(f"Go to Question {idx + 1}", key=f"review_goto_{idx}"):
                        st.session_state[f"quiz_completed_{self.name}"] = False
                        st.session_state[f"current_index_{self.name}"] = idx
                        st.rerun()
        else:
            st.success("Perfect score! You got all questions correct! 🌟")

        # Restart quiz button
        if st.button("Restart Quiz", key="restart_quiz"):
            st.session_state[f"answers_{self.name}"] = {}
            st.session_state[f"attempts_{self.name}"] = {}
            st.session_state[f"quiz_completed_{self.name}"] = False
            st.session_state[f"balloons_shown_{self.name}"] = False
            st.session_state[f"current_index_{self.name}"] = 0
            st.rerun()

    def drawOverview(self) -> None:
        """Draws the overview panel showing attempt statistics for each question."""
        st.title("📊 Quiz Overview")
        st.write("See how many attempts each question took:")
        
        attempts = st.session_state.get(f"attempts_{self.name}", {})
        answers = st.session_state.get(f"answers_{self.name}", {})
        
        # Create a container for the overview
        for idx, question in enumerate(self.question_list):
            attempt_count = attempts.get(idx, 0)
            answer_data = answers.get(idx, {})
            is_correct = answer_data.get("correct", False)
            
            # Determine status and styling
            if attempt_count == 0:
                status_icon = "⬜"
                status_text = "Not yet attempted"
            elif is_correct:
                status_icon = "✅"
                if attempt_count == 1:
                    status_text = "Correct on first try!"
                else:
                    status_text = f"Correct after {attempt_count} attempt{'s' if attempt_count > 1 else ''}"
            else:
                status_icon = "🔄"
                status_text = f"{attempt_count} attempt{'s' if attempt_count > 1 else ''} - still trying"
            
            # Create an expander for each question
            with st.expander(f"{status_icon} Question {idx + 1}: {question.title}", expanded=False):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    if attempt_count == 0:
                        st.info(status_text)
                    elif is_correct:
                        st.success(status_text)
                    else:
                        st.warning(status_text)
                
                with col2:
                    if st.button(f"Go to Q{idx + 1}", key=f"overview_goto_{idx}"):
                        st.session_state[f"show_overview_{self.name}"] = False
                        st.session_state[f"current_index_{self.name}"] = idx
                        st.rerun()
        
        # Summary statistics
        st.divider()
        total_questions = len(self.question_list)
        attempted_count = len([i for i in range(total_questions) if attempts.get(i, 0) > 0])
        correct_count = len([i for i in range(total_questions) if answers.get(i, {}).get("correct", False)])
        total_attempts = sum(attempts.values())
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Questions", f"{attempted_count}/{total_questions}")
        with col2:
            st.metric("Correct", correct_count)
        with col3:
            st.metric("Total Attempts", total_attempts)
        with col4:
            avg_attempts = total_attempts / attempted_count if attempted_count > 0 else 0
            st.metric("Avg Attempts", f"{avg_attempts:.1f}")
        
        st.divider()
        
        # Back button
        if st.button("← Back to Quiz", key="back_from_overview", type="primary"):
            st.session_state[f"show_overview_{self.name}"] = False
            st.rerun()

    def drawQuestionNavigator(self) -> None:
        """Draws numbered boxes at the bottom to navigate between questions."""
        if not self.question_list:
            return

        st.divider()

        BUTTONS_PER_ROW = 10

        chunks = [
            self.question_list[i : i + BUTTONS_PER_ROW]
            for i in range(0, len(self.question_list), BUTTONS_PER_ROW)
        ]

        button_index = 0
        for chunk in chunks:
            side_space = (BUTTONS_PER_ROW - len(chunk)) / 2
            cols = st.columns([side_space] + [1] * len(chunk) + [side_space])
            for col in cols[1:-1]:
                with col:
                    button_type = "primary" if button_index == self.current_index else "secondary"
                    if st.button(
                        str(button_index + 1),
                        key=f"question_nav_{self.name}_{button_index}",
                        type=button_type,
                        width="stretch",
                    ):
                        st.session_state[f"current_index_{self.name}"] = button_index
                        st.rerun()
                button_index += 1

        # Finish quiz button (only show when all questions answered)
        if self.isQuizComplete():
            st.divider()
            if st.button("Finish Quiz", key="finish_quiz", type="primary"):
                st.session_state[f"quiz_completed_{self.name}"] = True
                st.rerun()
        
        # Overview button - always visible
        st.divider()
        if st.button("📊 Overview", key="show_overview", help="View your progress and attempts for each question"):
            st.session_state[f"show_overview_{self.name}"] = True
            st.rerun()

    def drawPreviousButton(self) -> None:
        """Draws a button to go to the previous question."""

        def _previous_callback() -> None:
            st.session_state["current_index"] = st.session_state["current_index"] - 1

        if st.button("Previous", key="previous_button", on_click=_previous_callback):
            pass

    def drawNextButton(self) -> None:
        """Draws a button to go to the next question."""

        def _next_callback() -> None:
            st.session_state["current_index"] = st.session_state["current_index"] + 1

        if st.button("Next", key="next_button", on_click=_next_callback):
            pass

    def drawQuiz(self) -> None:
        """Draws the elements of the quiz."""
        # Show review page if quiz is completed
        if st.session_state.get(f"quiz_completed_{self.name}", False):
            self.drawReviewPage()
            return
        
        # Show overview if requested
        if st.session_state.get(f"show_overview_{self.name}", False):
            self.drawOverview()
            return

        self.current_index = st.session_state.get(f"current_index_{self.name}", 0)
        safe_index = min(self.current_index, len(self.question_list) - 1)
        QuestionDrawer.drawQuestion(self.question_list[safe_index], quiz=self, question_index=safe_index)
        self.drawQuestionNavigator()
