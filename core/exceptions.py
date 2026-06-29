class ERPAgentError(Exception):
    """Base exception for ERP AI Agent errors."""


class ERPValidationError(ERPAgentError):
    """Raised when user input or extracted parameters are invalid."""


class ERPAPIError(ERPAgentError):
    """Raised when ERP data cannot be loaded or accessed."""
