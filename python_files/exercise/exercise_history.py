class ExerciseHistory:
    def __init__(self, exercise_index, exercise_name, start_time, end_time=0, exercised_time=0, use_kcal=0, count=0, coin=0):
        self.exercise_index = exercise_index
        self.exercise_name = exercise_name
        self.start_time = start_time
        self.end_time = end_time
        self.exercised_time = exercised_time
        self.use_kcal = use_kcal
        self.count = count
        self.coin = coin