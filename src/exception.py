import sys

def error_message_detail(error, error_detail: sys):
  _,_,exc_tb = error_detail.exc_info() # exc_info() is a function in the sys module that returns a tuple containing information about the current exception being handled. The tuple contains three values: the exception type, the exception value, and the traceback object. By unpacking the tuple into three variables, we can access the specific details of the exception that occurred. exc_tb is the traceback object that contains information about the call stack at the point where the exception was raised. This can be useful for debugging purposes, as it allows us to see the sequence of function calls that led to the error.
  
  file_name = exc_tb.tb_frame.f_code.co_filename  # tb_frame is an attribute of the traceback object that represents the current stack frame. f_code is an attribute of the frame object that contains information about the code being executed in that frame. co_filename is an attribute of the code object that contains the name of the file where the code is located. By accessing these attributes, we can retrieve the name of the file where the exception occurred, which can be helpful for debugging and understanding the context of the error.
  error_message =f"Error occured python script name{0} line number[{1}] error message[{2}]".format(
    file_name, exc_tb.tb_lineno, str(error)
  )
  return error_message






class CustomException(Exception): # making a custom exception class that inherits from the built-in Exception class.
  def __init__(self, error_message, error_detail: sys): 
    super().__init__(error_message)
    self.error_message = error_message_detail(
      error_message, error_detail=error_detail
    )
  def __str__(self):
    return self.error_message