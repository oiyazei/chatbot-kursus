class DialogManager:
    def __init__(self, answer_path):
        import json
        with open(answer_path, 'r', encoding='utf-8') as f:
            self.answers = json.load(f)["intents"]
        self.state = {}

    def update_state(self, user_id, intent):
        self.state[user_id] = {"last_intent": intent}

    def get_last_intent(self, user_id):
        return self.state.get(user_id, {}).get("last_intent", None)

    def get_response(self, intent):
        for item in self.answers:
            if item["intent"] == intent:
                return item["responses"][0]
        return "Maaf, saya tidak mengerti maksud kamu."