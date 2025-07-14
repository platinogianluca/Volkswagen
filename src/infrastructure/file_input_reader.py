class FileInputReader:
    def get_input(self, file_path: str) -> str:
        try:
            with open(file_path, "r") as file:
                return file.read()
        except FileNotFoundError:
            raise FileNotFoundError(
                f"Input file '{file_path}' not found. "
                "Please create it with the required input format."
            )