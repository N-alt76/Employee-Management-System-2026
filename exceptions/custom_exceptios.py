class EmployeeError(Exception):
	"""Base exception for employee-management errors."""


class EmployeeValidationError(EmployeeError):
	"""Raised when employee input is invalid."""


class EmployeeNotFoundError(EmployeeError):
	"""Raised when an employee does not exist."""
