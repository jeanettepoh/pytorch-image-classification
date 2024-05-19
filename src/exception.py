import sys


def error_message_detail(error: Exception, error_detail:sys) -> str:
    _, _, exc_tb = error_detail.exc_info()
    if exc_tb.tb_frame is not None and exc_tb.tb_lineno is not None:
        filename: str = exc_tb.tb_frame.f_code.co_filename
        error_message = "Error occurred in Python script '{0}' at line number {1}: {2}".format(
            filename, exc_tb.tb_lineno, str(error)
        )
    else:
        error_message = "Error occurred: {0}".format(str(error))
    return error_message


class CustomException(Exception):
    def __init__(self, error_message, error_detail):
        super().__init__(error_message)
        self.error_message: str = error_message_detail(
            error_message, error_detail
        )

    def __str__(self):
        return self.error_message