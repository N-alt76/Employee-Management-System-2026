from exceptions.custom_exceptios import EmployeeNotFoundError, EmployeeValidationError
from exceptions.database.db import get_connection
from models.employee import Employee


def _validated_data(data):
	fields = ("name", "email", "department", "role", "salary")
	values: dict[str, str | float] = {
		field: str(data.get(field, "")).strip() for field in fields
	}
	if any(not values[field] for field in fields[:-1]):
		raise EmployeeValidationError("Name, email, department, and role are required.")
	try:
		values["salary"] = float(values["salary"])
	except ValueError as error:
		raise EmployeeValidationError("Salary must be a valid number.") from error
	if values["salary"] < 0:
		raise EmployeeValidationError("Salary cannot be negative.")
	return values


def list_employees():
	with get_connection() as connection:
		rows = connection.execute(
			"SELECT * FROM employees ORDER BY name COLLATE NOCASE"
		).fetchall()
	return [Employee.from_row(row) for row in rows]


def create_employee(data):
	values = _validated_data(data)
	try:
		with get_connection() as connection:
			cursor = connection.execute(
				"""
				INSERT INTO employees (name, email, department, role, salary)
				VALUES (:name, :email, :department, :role, :salary)
				""",
				values,
			)
			employee_id = cursor.lastrowid
	except Exception as error:
		if "UNIQUE constraint failed" in str(error):
			raise EmployeeValidationError("An employee with this email already exists.") from error
		raise
	return get_employee(employee_id)


def get_employee(employee_id):
	with get_connection() as connection:
		row = connection.execute(
			"SELECT * FROM employees WHERE id = ?", (employee_id,)
		).fetchone()
	if row is None:
		raise EmployeeNotFoundError("Employee not found.")
	return Employee.from_row(row)


def update_employee(employee_id, data):
	values = _validated_data(data)
	with get_connection() as connection:
		cursor = connection.execute(
			"""
			UPDATE employees
			SET name = :name, email = :email, department = :department,
				role = :role, salary = :salary
			WHERE id = :id
			""",
			{**values, "id": employee_id},
		)
	if cursor.rowcount == 0:
		raise EmployeeNotFoundError("Employee not found.")
	return get_employee(employee_id)


def delete_employee(employee_id):
	with get_connection() as connection:
		cursor = connection.execute("DELETE FROM employees WHERE id = ?", (employee_id,))
	if cursor.rowcount == 0:
		raise EmployeeNotFoundError("Employee not found.")
