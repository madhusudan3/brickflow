if __name__ == "__main__":
    import re

    # string = "class Artifacts1(BaseModel)"
    regex_pattern = r"(?<=class\s)[A-Za-z]\w+"
    file_path = "brickflow/bundles/model.py"

    bad_class_names = {}

    def remove_number_from_end(string):
        match = re.search(r"\d+$", string)
        if match:
            number = match.group(0)
            string_without_number = string[: -len(number)]
            return string_without_number
        else:
            return None

    def remove_timestamp_line(input_code: str) -> str:
        return "\n".join(
            [
                _line
                for _line in input_code.split("\n")
                if not _line.startswith("#   timestamp: ")
            ]
        )

    def replace_class_config_extras(input_code: str) -> str:
        pattern = r"extra\s*=\s*Extra\.forbid"
        return re.sub(
            pattern, 'extra = "forbid"\n        protected_namespaces = ()', input_code
        )

    def replace_regex_with_pattern(input_code: str) -> str:
        pattern = r"regex="
        return re.sub(pattern, "pattern=", input_code)

    with open(file_path, "r") as f:
        lines = f.readlines()
        for line in lines:
            match = re.search(regex_pattern, line)
            if match:
                dynamic_value = match.group(0)
                if remove_number_from_end(dynamic_value):
                    bad_class_names[dynamic_value] = remove_number_from_end(
                        dynamic_value
                    )

    with open(file_path, "r") as r:
        data = r.read()

        with open(file_path, "w") as w:
            for key, value in bad_class_names.items():
                data = data.replace(key, value)
            data = remove_timestamp_line(data)
            # remove extra config to remove deprecation warning
            data = replace_class_config_extras(data)
            # replace regex with pattern
            data = replace_regex_with_pattern(data)
            w.write(data)
