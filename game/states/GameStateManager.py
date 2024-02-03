class GameStateManager:
    def change_state(self, new_state):
        self.current_state = self.states[new_state]()
        self.current_state.enter()