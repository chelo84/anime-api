class ListUtil(object):
    @staticmethod
    def filter_list(function, list_to_filter):
        return list(
            filter(
                function,
                list_to_filter
            )
        )

    @staticmethod
    def get_only_specific_fields(result, fields):
        elements = []
        if fields and len(fields) > 0:
            for r in result:
                element = {}
                for field in fields:
                    element[field] = r[field.strip()]

                elements.append(element)
        else:
            elements = result

        return elements
