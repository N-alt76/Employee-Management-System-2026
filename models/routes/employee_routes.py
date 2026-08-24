from flask import Blueprint, jsonify, request

from exceptions.custom_exceptios import EmployeeError
from services.employee_services import (
	create_employee,
	delete_employee,
	list_employees,
	update_employee,
)


employee_routes = Blueprint("employees", __name__, url_prefix="/api/employees")


@employee_routes.get("")
def employees():
	return jsonify([employee.to_dict() for employee in list_employees()])


@employee_routes.post("")
def add_employee():
	try:
		employee = create_employee(request.get_json(silent=True) or {})
		return jsonify(employee.to_dict()), 201
	except EmployeeError as error:
		return jsonify({"error": str(error)}), 400


@employee_routes.put("/<int:employee_id>")
def edit_employee(employee_id):
	try:
		employee = update_employee(employee_id, request.get_json(silent=True) or {})
		return jsonify(employee.to_dict())
	except EmployeeError as error:
		status = 404 if error.__class__.__name__ == "EmployeeNotFoundError" else 400
		return jsonify({"error": str(error)}), status


@employee_routes.delete("/<int:employee_id>")
def remove_employee(employee_id):
	try:
		delete_employee(employee_id)
		return "", 204
	except EmployeeError as error:
		return jsonify({"error": str(error)}), 404
