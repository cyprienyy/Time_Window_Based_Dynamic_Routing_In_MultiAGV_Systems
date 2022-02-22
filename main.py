from collections import defaultdict
from operator import itemgetter
import bisect


class Mission:
    def __init__(self):
        self.index = None
        self.mission_type = 1  # 1:真实执行的任务；0：空车调度任务
        self.o_arc = None
        self.d_arc = None
        self.shortest_feasible_path = None
        self.prior_0 = None
        self.prior_t = None
        self.vehicle = None  # 可能导致内存无法释放，暂时不使用
        self.created_time = None
        self.assigned_time = None
        return

    def calculate_prior_t(self) -> float:
        return 1.0

    def get_time_win_of_arc(self, arc, mission, t_m, direction):
        return self.shortest_feasible_path.get_time_win_of_arc(arc, mission, t_m, direction)


class Vehicle:
    def __init__(self, index, loc):
        self.index = index
        self.status = 0  # 2：正在执行真实任务；1：正在执行空车调度任务；0：原地待命
        self.mission = None
        self.loc = loc
        self.free_time_recorder = list()

    def assign_mission(self, mission: Mission, t):
        if mission.mission_type == 1:
            self.status = 2
        elif mission.mission_type == 1:
            self.status = 1
        else:
            raise Exception('未识别的任务类型')
        return

    def remove_mission(self, t):
        self.mission = None
        self.status = 0

    def is_open_for_real_mission(self) -> bool:
        if self.status in (0, 1):
            return True
        return False

    def is_resting_on_arc(self, arc) -> bool:
        if self.status == 0 and self.loc == arc:
            return True

    def get_time_win_of_arc(self, arc, mission, t_m, direction):
        if self.mission is not None:
            return self.mission.get_time_win_of_arc(arc, mission, t_m, direction)
        return None


class Path:

    @staticmethod
    def default_time_vector():
        return [0, float('inf'), float('inf')]

    def __init__(self):
        self.arcs = list()
        self.arc_2_time_windows = defaultdict(self.default_time_vector)

    def get_finish_time(self):
        return self.arc_2_time_windows[self.arcs[-1]][-1]

    def get_time_win_of_arc(self, arc, mission, t_m, direction):
        if arc in self.arc_2_time_windows.keys():
            time_win = self.arc_2_time_windows[arc].copy()
            if time_win[-1] >= t_m:
                return time_win
        return None


class MainAlgorithm:
    def __init__(self):
        self.active_missions = list()
        self.arc_pair_rel = dict()
        self.vehicles = list()
        self.wait_missions = list()
        self.parking_spaces = dict()  # 0：空闲；1：占用
        return

    def add_vehicle(self, vehicle_num: int, vehicle_locs: list):
        for i, _loc in zip(range(vehicle_num), vehicle_locs):
            self.vehicles.append(Vehicle(i, _loc))
        return

    def create_idle_positioning_mission(self, vehicle: Vehicle, origin, t):
        des = None
        # 找出空的停车位
        for lot, status in self.parking_spaces.items():
            if status == 0:
                des = lot
                break
        if des is not None:
            # 先创建一个任务
            mission = Mission()
            mission.o_arc = origin  # 应该要是车辆的当前位置
            mission.d_arc = des
            mission.created_time = t
            mission.mission_type = 0
            # 为该任务选择路径
            # 把路径交给任务
            # 把任务交给车辆
        else:
            raise Exception('No Empty Parking Space')
        return

    def calculate_initial_mission_priority(self, mission: Mission) -> float:
        return 1.0

    def create_new_mission(self):
        return

    def mission_completed(self, vehicle: Vehicle, t):
        vehicle.remove_mission(t)
        return

    def mission_arrive(self, index, origin, destination, t):
        mission = Mission()
        mission.index = index
        mission.o_arc = origin
        mission.d_arc = destination
        mission.created_time = t
        self.wait_missions.append(mission)
        return

    def

    def get_time_vectors_of_arc(self, arc, mission: Mission, vehicle: Vehicle, t_m):
        rev_arc = self.arc_pair_rel[arc]
        res = list()
        for _v in self.vehicles:
            if _v != vehicle:
                win_1 = _v.get_time_win_of_arc(arc, mission, t_m, 1)
                win_2 = _v.get_time_win_of_arc(rev_arc, mission, t_m, -1)
                if win_1 is not None:
                    res.append(win_1)
                if win_2 is not None:
                    res.append(win_2)
        res.sort(key=itemgetter(0))
        return zip(*res)

    @staticmethod
    def temp_get_time_vector(arc):
        temp_dict = dict()
        temp_dict['a'] = [[40, 230], [110, 240]]
        temp_dict['b'] = [[200, 280, 340], [225, 300, 500]]
        temp_dict['c'] = [[0], [280]]
        if arc in temp_dict:
            return temp_dict[arc]
        else:
            return [], []

    def shortest_path_with_time_windows(self, t_m, mission: Mission, _vehicles: list):
        # choose_available_vehicles()
        if _vehicles is None:
            vehicles = self.vehicles
        else:
            vehicles = _vehicles
        best_v = None
        best_path = None
        earliest_finish_time = float('inf')
        for v in vehicles:
            for p in get_offline_paths():
                flag, path = self.validate_path(mission, p, v, t_m)
            if flag is True:
                p_f_time = path.get_finish_time()
                if p_f_time < earliest_finish_time:
                    best_v = v
                    best_path = path
                    earliest_finish_time = p_f_time
        return best_v, best_path

    def reschedule_low_priority_missions(self):
        return

    def validate_path(self, mission: Mission, path: Path, vehicle: Vehicle, t_m):

        # # 定义每一段小弧对应的起始弧
        # arc_start_arc = dict()

        buffer_in_t_j = dict()
        buffer_out_t_j = dict()

        o_m = path.arcs[0]
        in_t_o_m, out_t_o_m = self.temp_get_time_vector(o_m)
        buffer_in_t_j[o_m] = in_t_o_m
        buffer_out_t_j[o_m] = out_t_o_m

        path.arc_2_time_windows[o_m][1] = t_m
        path.arc_2_time_windows[o_m][2] = t_m + path.arc_2_time_windows[o_m][0]

        arc_p = dict()  # 每个小弧在时间窗内的插入位置
        arc_p[o_m] = -2
        #
        if in_t_o_m:  # 判断是否会受其他车辆影响
            if t_m <= in_t_o_m[0]:
                arc_p[o_m] = -1
            for i in range(0, len(in_t_o_m) - 1):
                if out_t_o_m[i] <= t_m <= in_t_o_m[i + 1]:
                    arc_p[o_m] = i
            if t_m >= out_t_o_m[-1]:
                arc_p[o_m] = len(in_t_o_m)
        else:  # 不受影响，直接插入
            arc_p[o_m] = 0
        if arc_p[o_m] == -2:
            return '初始弧无法插入', None
        #
        for arc in path.arcs[1:]:
            arc_p[arc] = -2
        # """

        arc_num = len(path.arcs)
        j = 1

        while j < arc_num:

            arc = path.arcs[j]

            # w_j = []
            if arc in buffer_in_t_j:
                in_t_j = buffer_in_t_j[arc]
                out_t_j = buffer_out_t_j[arc]
            else:
                in_t_j, out_t_j = self.temp_get_time_vector(arc)
                buffer_in_t_j[arc] = in_t_j
                buffer_out_t_j[arc] = out_t_j

            out_t_mi = path.arc_2_time_windows[path.arcs[j - 1]][1] + path.arc_2_time_windows[path.arcs[j - 1]][0]
            w_mj = path.arc_2_time_windows[arc][0]
            # epsilon_m_j = 0.01 * w_mj
            epsilon_m_j = 5
            insert_success = False
            if not in_t_j:  # 不受影响，直接插入
                in_t_mj = path.arc_2_time_windows[arc][1] = out_t_mi
                out_t_mj = path.arc_2_time_windows[arc][2] = in_t_mj + w_mj
                arc_p[arc] = 0
            else:
                # start_arc = arc_start_arc[arc]
                # if start_arc == arc:
                # 是大路段中的起始小弧，可以随意决定插入位置
                if arc_p[arc] == -2 and in_t_j[0] - t_m > w_mj + epsilon_m_j \
                        and in_t_j[0] - w_mj - epsilon_m_j > out_t_mi:
                    in_t_mj = path.arc_2_time_windows[arc][1] = out_t_mi
                    out_t_mj = path.arc_2_time_windows[arc][2] = in_t_mj + w_mj
                    insert_success = True
                    arc_p[arc] = -1
                else:
                    for i in range(max(0, arc_p[arc]), len(in_t_j) - 1):
                        if in_t_j[i + 1] - max(out_t_j[i], out_t_mi) > w_mj + 2 * epsilon_m_j:
                            in_t_mj = path.arc_2_time_windows[arc][1] = max(out_t_j[i] + epsilon_m_j, out_t_mi)
                            out_t_mj = path.arc_2_time_windows[arc][2] = in_t_mj + w_mj
                            insert_success = True
                            arc_p[arc] = i
                            break
                if insert_success is False:
                    if out_t_j[-1] != float('inf'):
                        in_t_mj = path.arc_2_time_windows[arc][1] = max(out_t_j[-1] + epsilon_m_j, out_t_mi)
                        out_t_mj = path.arc_2_time_windows[arc][2] = in_t_mj + w_mj
                        arc_p[arc] = len(in_t_j)
                        insert_success = True
                    else:
                        return False, '弧' + str(arc) + '被占用'
                # else:
                #     # 不是起始小弧，那么必须与同一大路段中的起始小弧插入

            old_arc = path.arcs[j - 1]
            path.arc_2_time_windows[old_arc][2] = in_t_mj
            old_in_t_j = buffer_in_t_j[old_arc]
            # print('比较', path.arc_2_time_windows[old_arc][2], '与', old_in_t_j[arc_p[old_arc] + 1])
            if arc_p[old_arc] < len(old_in_t_j) - 1 \
                    and path.arc_2_time_windows[old_arc][2] > old_in_t_j[arc_p[old_arc] + 1]:
                if j == 1:
                    return False, '初始弧无法插入'
                else:
                    arc_p[old_arc] += 1
                    j = j - 1
            else:
                j = j + 1

        # """

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
        """
        return True, path


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
