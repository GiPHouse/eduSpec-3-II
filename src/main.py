from managers.QuestionManager import QuestionManager
from QuestionDrawer import QuestionDrawer
from managers.QuestionManager import QuestionManager
from navigation import initTheme, resolveQuestion, showNavigation

query_params = st.query_params
requested_question = query_params.get("question")
session_question = st.session_state.get("current_question")
current_question_name = resolveQuestion(requested_question or session_question)

st.session_state["current_question"] = current_question_name
if requested_question != current_question_name:
    st.query_params["question"] = current_question_name

initTheme()
showNavigation()

question = QuestionManager.loadQuestion(current_question_name)
QuestionDrawer.drawQuestion(question)
