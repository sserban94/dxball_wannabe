class GameStateManager:
    def __init__(self, game):
        self.game = game
        self.states = {}
        self.current_state = None

    def add_state(self, state_name, state_class):
        self.states[state_name] = state_class(self.game)

    def change_state(self, state_name):
        if state_name in self.states:
            if self.current_state is not None:
                print(f"Exiting state - {self.current_state} ")
                self.current_state.exit()
            self.current_state = self.states[state_name]
            print(f"Entering state - {state_name} ")
            self.current_state.enter()
        else:
            print(f"State {state_name} not found.")

    def update(self):
        if self.current_state:
            self.current_state.update()

    def handle_events(self):
        if self.current_state:
            self.current_state.handle_events()

    def render(self):
        if self.current_state:
            self.current_state.render()