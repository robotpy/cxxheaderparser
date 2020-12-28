from dataclasses import dataclass


@dataclass
class ParserOptions:
    """
    Options that control parsing behaviors
    """

    #: If true, prints out
    verbose: bool = False

    #: If true, converts a single void parameter to zero parameters
    convert_void_to_zero_params: bool = True
