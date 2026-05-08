import sys
import traceback


class CustomException(Exception):
    """
    Custom exception class for the project.

    Captures:
    - Error message
    - File name
    - Line number
    - Full traceback
    """

    def __init__(self, error_message: str, error_detail: sys = None):
        super().__init__(error_message)

        self.error_message = error_message
        self.error_detail = error_detail

        if error_detail:
            _, _, exc_tb = error_detail.exc_info()
            self.file_name = exc_tb.tb_frame.f_code.co_filename
            self.line_number = exc_tb.tb_lineno
        else:
            self.file_name = None
            self.line_number = None

    def __str__(self):
        if self.file_name and self.line_number:
            return (
                f"Error: {self.error_message} | "
                f"File: {self.file_name} | "
                f"Line: {self.line_number}"
            )
        return f"Error: {self.error_message}"


def format_traceback() -> str:
    """
    Returns full traceback as string.
    Useful for logging/debugging.
    """

    return traceback.format_exc()


def raise_custom_exception(error_message: str):
    """
    Helper function to raise exception with traceback.
    """

    raise CustomException(error_message, sys)