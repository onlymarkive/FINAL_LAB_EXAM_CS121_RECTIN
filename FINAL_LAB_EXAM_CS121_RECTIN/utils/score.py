class Score:
    def __init__(self, username, formatted_datetime, game_id, points=0, wins=0):
        self.username = username
        self.formatted_datetime = formatted_datetime
        self.game_id = game_id
        self.points = points
        self.wins = wins