class ListUtil(object):
    @staticmethod
    def filter_list(function, list_to_filter):
        return list(
            filter(
                function,
                list_to_filter
            )
        )
