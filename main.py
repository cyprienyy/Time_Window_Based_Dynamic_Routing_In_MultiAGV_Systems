from collections import defaultdict


class Mission:
    def __init__(self):
        self.index = None
        self.mission_type = None  # 真实需要执行的任务，reposition任务
        self.o_arc = None
        self.d_arc = None
        self.shortest_feasible_path = None
        self.prior_0 = None
        self.prior_t = None
        self.vehicle = None
        return

    def calculate_prior_t(self) -> None:
        return


class Vehicle:
    def __init__(self):
        self.index = None
        self.status = None  # 正在执行真实任务，正在执行reposition任务，无任务
        return


class Path:

    @staticmethod
    def default_time_vector():
        return [0, float('inf'), float('inf')]

    def __init__(self):
        self.arcs = list()
        self.arc_2_time_vectors = defaultdict()


class MainAlgorithm:
    def __init__(self):
        return

    def create_idle_positioning_mission(self):
        return

    def calculate_initial_mission_priority(self, mission: Mission) -> float:
        return

    def create_new_mission(self):
        return

    def mission_completed(self):
        return

    def mission_arrive(self):
        create_new_mission()
        shortest_path_with_time_windows()
        apply_selected_path()
        return

    def get_time_vectors_of_arc(self):
        return

    def shortest_path_with_time_windows(self):
        choose_available_vehicles()
        get_offline_paths()
        for path in candidate_paths:
            validate_path()
        return

    def reschedule_low_priority_missions(self):
        return

    def validate_path(self, mission: Mission, path, vehicle, t_m):

        in_t_o_m = []
        out_t_o_m = []

        for arc in path_arcs[1:]:
            w_j = []
            in_t_j = []
            out_t_j = []

            insert_time_window()

        backtrack_time_windows()

        while check_new_time_vectors_for_overlap():
            for arc in path_arcs[q:]:
                insert_time_window()
