class GlobalsError(Exception):
    """Error, no global variables."""

    pass


class EndpointAnswerException(Exception):
    """Error, no answer from Endpoint."""

    pass


class CheckResponseException(Exception):
    """Error, not correct answer from Endpoint."""

    pass


class ParseStatusException(Exception):
    """Error, incorrect homework status."""

    pass
