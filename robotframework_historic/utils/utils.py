class Utils:
    @staticmethod
    def sort_tests(data_list):
        out = {}
        for elem in data_list:
            try:
                out[elem[0]].extend(elem[1:])
            except KeyError:
                out[elem[0]] = list(elem)
        return [tuple(values) for values in out.values()]

    @staticmethod
    def get_count_by_perc(data_list, max, min):
        count = 0
        for item in data_list:
            if max >= item[0] >= min:
                count += 1
        return count
