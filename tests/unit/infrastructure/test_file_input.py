import pytest
from unittest.mock import mock_open, patch

from src.infrastructure.file_input_reader import FileInputReader


class TestFileInputAdapter:

    def setup_method(self):
        self.adapter = FileInputReader()

    @patch("builtins.open", new_callable=mock_open)
    def test_example(self, mock_file):
        # Configurar manualmente qué retorna read()
        mock_file.return_value.read.return_value = "test content"
        
        result = self.adapter.get_input("file.txt")
        assert result == "test content" 

   
    @patch("builtins.open", side_effect=FileNotFoundError)
    def test_get_input_file_not_found_raises_error(self, mock_file):
        # Arrange
        file_path = "nonexistent_file.txt"
        expected_message = (
            f"Input file '{file_path}' not found. "
            "Please create it with the required input format."
        )

        # Act & Assert
        with pytest.raises(FileNotFoundError) as exc_info:
            self.adapter.get_input(file_path)

        mock_file.assert_called_once_with(file_path, "r")
        assert str(exc_info.value) == expected_message