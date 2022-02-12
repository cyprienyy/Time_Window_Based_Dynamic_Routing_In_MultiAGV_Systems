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
        self.arc_2_time_windows = defaultdict(self.default_time_vector)


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
        # create_new_mission()
        # shortest_path_with_time_windows()
        # apply_selected_path()
        return

    def get_time_vectors_of_arc(self, arc, mission: Mission, t_m):

        return

    def temp_get_time_vector(self, arc):
        self._dict = dict()
        self._dict['a'] = [[40, 230], [110, 240]]
        self._dict['b'] = [[200, 280, 340], [225, 300, 500]]
        self._dict['c'] = [[0], [280]]
        if arc in self._dict:
            return self._dict[arc]
        else:
            return [], []

    def shortest_path_with_time_windows(self):
        # choose_available_vehicles()
        # get_offline_paths()
        # for path in candidate_paths:
        #     validate_path()
        return

    def reschedule_low_priority_missions(self):
        return

    def validate_path(self, mission: Mission, path: Path, vehicle: Vehicle, t_m):

        buffer_in_t_j = dict()
        buffer_out_t_j = dict()

        o_m = path.arcs[0]
        in_t_o_m, out_t_o_m = self.temp_get_time_vector(o_m)
        buffer_in_t_j[o_m] = in_t_o_m
        buffer_out_t_j[o_m] = out_t_o_m

        path.arc_2_time_windows[o_m][1] = t_m
        path.arc_2_time_windows[o_m][2] = t_m + path.arc_2_time_windows[o_m][0]

        arc_p = dict()
        arc_p[o_m] = -2
        #
        if in_t_o_m:
            if t_m <= in_t_o_m[0]:
                arc_p[o_m] = -1
            for i in range(0, len(in_t_o_m) - 1):
                if out_t_o_m[i] <= t_m <= in_t_o_m[i + 1]:
                    arc_p[o_m] = i
            if t_m >= out_t_o_m[-1]:
                arc_p[o_m] = len(in_t_o_m)
        else:
            arc_p[o_m] = 0
        if arc_p[o_m] == -2:
            return '初始弧无法插入', None
        #
        for arc in path.arcs[1:]:
            arc_p[arc] = -1

        """
        
        arc_num = len(path.arcs)
        j = 1
        
        while j < arc_num:

            arc = path.arcs[j]

            # w_j = []
            if buffer_in_t_j.has_key(arc):
                in_t_j = buffer_in_t_j[arc]
                out_t_j = buffer_out_t_j[arc]
            else:
                in_t_j = []
                out_t_j = []
                buffer_in_t_j[arc] = in_t_j
                buffer_out_t_j[arc] = out_t_j

            out_t_mi = path.arc_2_time_windows[path.arcs[j - 1]][1] + path.arc_2_time_windows[path.arcs[j - 1]][0] 
            w_mj = path.arc_2_time_windows[arc][0]
            epsilon_m_j = 0.01 * w_mj
            if arc_p[arc] < 0 and in_t_j[0] - t_m > w_mj + epsilon_m_j and in_t_j[0] - w_mj + epsilon_m_j > out_t_mi:
                in_t_mj = path.arc_2_time_windows[arc][1] = out_t_mi
                out_t_mj = path.arc_2_time_windows[arc][2] = in_t_mj + w_mj
                # arc_p[arc] = 0 
            else:
                insert_success = False
                for i in range(max(0,arc_p[arc]), len(in_t_j) - 1):
                    if in_t_j[i + 1] - max(out_t_j[i], out_t_mi) > w_mj + 2 * epsilon_m_j:
                        in_t_mj = path.arc_2_time_windows[arc][1] = max(out_t_j[i] + epsilon_m_j, out_t_mi)
                        out_t_mj = path.arc_2_time_windows[arc][2] = in_t_mj + w_mj
                        insert_success = True
                        arc_p[arc] = i
                        # arc_p[arc] = i + 1
                        break
            if insert_success is False:
                in_t_mj = path.arc_2_time_windows[arc][1] = max(out_t_j[-1] + epsilon_m_j, out_t_mi)
                out_t_mj = path.arc_2_time_windows[arc][2] = in_t_mj + w_mj
                arc_p[arc] = len(in_t_j)

            old_arc = path.arcs[j - 1]
            path.arc_2_time_windows[old_arc][2] = in_t_mj
            old_in_t_j = buffer_in_t_j[old_arc]
            if arc_p[old_arc] < len(old_in_t_j) \
                    and path.arc_2_time_windows[old_arc][2] < old_in_t_j[arc_p[old_arc]]:
                if j == 1:
                    return False, None
                else:
                    arc_p[old_arc] += 1
                    j = j - 1
            else:
                j = j + 1
        """

        start_arc = 1
        while True:
            for j, arc in enumerate(path.arcs[start_arc:], start=start_arc):
                # w_j = []
                if arc in buffer_in_t_j:
                    in_t_j, out_t_j = buffer_in_t_j[arc], buffer_out_t_j[arc]
                else:
                    in_t_j, out_t_j = self.temp_get_time_vector(arc)
                    buffer_in_t_j[arc] = in_t_j
                    buffer_out_t_j[arc] = out_t_j

                out_t_mi = path.arc_2_time_windows[path.arcs[j - 1]][1] + path.arc_2_time_windows[path.arcs[j - 1]][0]
                w_mj = path.arc_2_time_windows[arc][0]
                # epsilon_m_j = 0.01 * w_mj
                epsilon_m_j = 5

                if not in_t_j:
                    in_t_mj = path.arc_2_time_windows[arc][1] = out_t_mi
                    out_t_mj = path.arc_2_time_windows[arc][2] = in_t_mj + w_mj

                    path.arc_2_time_windows[path.arcs[j - 1]][2] = in_t_mj
                    arc_p[arc] = 0

                    continue

                if in_t_j[0] - t_m > w_mj + epsilon_m_j and in_t_j[0] - (w_mj + epsilon_m_j) > out_t_mi:
                    in_t_mj = path.arc_2_time_windows[arc][1] = out_t_mi
                    out_t_mj = path.arc_2_time_windows[arc][2] = in_t_mj + w_mj

                    path.arc_2_time_windows[path.arcs[j - 1]][2] = in_t_mj
                    arc_p[arc] = -1

                    continue
                insert_success = False
                for i in range(len(in_t_j) - 1):
                    if in_t_j[i + 1] - max(out_t_j[i], out_t_mi) > w_mj + 2 * epsilon_m_j:
                        in_t_mj = path.arc_2_time_windows[arc][1] = max(out_t_j[i] + epsilon_m_j, out_t_mi)
                        out_t_mj = path.arc_2_time_windows[arc][2] = in_t_mj + w_mj

                        path.arc_2_time_windows[path.arcs[j - 1]][2] = in_t_mj
                        arc_p[arc] = i

                        insert_success = True
                        break
                if insert_success:
                    continue
                in_t_mj = path.arc_2_time_windows[arc][1] = max(out_t_j[-1] + epsilon_m_j, out_t_mi)
                out_t_mj = path.arc_2_time_windows[arc][2] = in_t_mj + w_mj

                path.arc_2_time_windows[path.arcs[j - 1]][2] = in_t_mj
                arc_p[arc] = len(in_t_j)

            overlap = False
            overlap_arc = -1
            for j, arc in enumerate(path.arcs):
                # w_j = []

                if arc in buffer_in_t_j:
                    in_t_j, out_t_j = buffer_in_t_j[arc], buffer_out_t_j[arc]
                else:
                    in_t_j, out_t_j = self.temp_get_time_vector(arc)
                    buffer_in_t_j[arc] = in_t_j
                    buffer_out_t_j[arc] = out_t_j

                p = arc_p[arc]
                if p < len(in_t_j) - 1 and path.arc_2_time_windows[arc][2] > in_t_j[p + 1]:
                    overlap = True
                    overlap_arc = j
                    break
            if overlap_arc == 0:
                return '起始弧有重叠', None
            if overlap is False:
                break

            j = overlap_arc
            arc = path.arcs[overlap_arc]
            in_t_j, out_t_j = self.temp_get_time_vector(arc)
            out_t_mi = path.arc_2_time_windows[path.arcs[j - 1]][1] + path.arc_2_time_windows[path.arcs[j - 1]][0]
            w_mj = path.arc_2_time_windows[arc][0]
            # epsilon_m_j = 0.01 * w_mj
            epsilon_m_j = 5
            insert_success = False
            for i in range(arc_p[arc] + 1, len(in_t_j) - 1):
                if in_t_j[i + 1] - max(out_t_j[i], out_t_mi) > w_mj + 2 * epsilon_m_j:
                    in_t_mj = path.arc_2_time_windows[arc][1] = max(out_t_j[i] + epsilon_m_j, out_t_mi)
                    out_t_mj = path.arc_2_time_windows[arc][2] = in_t_mj + w_mj

                    path.arc_2_time_windows[path.arcs[j - 1]][2] = in_t_mj
                    arc_p[arc] = i

                    insert_success = True
                    break
            if insert_success is False:
                in_t_mj = path.arc_2_time_windows[arc][1] = max(out_t_j[-1] + epsilon_m_j, out_t_mi)
                out_t_mj = path.arc_2_time_windows[arc][2] = in_t_mj + w_mj

                path.arc_2_time_windows[path.arcs[j - 1]][2] = in_t_mj
                arc_p[arc] = len(in_t_j)

            start_arc = overlap_arc + 1


if __name__ == "__main__":
    _path = Path()
    _path.arcs = ['a', 'b', 'c']
    _path.arc_2_time_windows['a'] = [100, -1, -1]
    _path.arc_2_time_windows['b'] = [30, -1, -1]
    _path.arc_2_time_windows['c'] = [50, -1, -1]

    _t_m = 120
    _mission = Mission()
    _vehicle = Vehicle()
    _algorithm = MainAlgorithm()
    _res, _ = _algorithm.validate_path(_mission, _path, _vehicle, _t_m)
    print(_res)
    print('finished')
