from typing import Dict


class ConversationMemory:

    def __init__(self):
        self.sessions: Dict[str, Dict] = {}

    def get_session(self, session_id: str):

        if session_id not in self.sessions:
            self.sessions[session_id] = {
                "problem": None,
                "profile": {}
            }

        return self.sessions[session_id]

    def update_problem(
        self,
        session_id: str,
        problem: str
    ):

        session = self.get_session(session_id)

        session["problem"] = problem

    def update_profile(
        self,
        session_id: str,
        profile: Dict
    ):

        session = self.get_session(session_id)

        for key, value in profile.items():

            if value is not None and value != "":
                session["profile"][key] = value

    def get_context(self, session_id: str):

        return self.get_session(session_id)

    def clear_session(self, session_id: str):

        if session_id in self.sessions:
            del self.sessions[session_id]