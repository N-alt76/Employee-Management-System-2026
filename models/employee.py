from dataclasses import dataclass


@dataclass
class Employee:
	name: str
	email: str
	department: str
	role: str
	salary: float
	id: int | None = None
	created_at: str | None = None

	@classmethod
	def from_row(cls, row):
		return cls(
			id=row["id"],
			name=row["name"],
			email=row["email"],
			department=row["department"],
			role=row["role"],
			salary=row["salary"],
			created_at=row["created_at"],
		)

	def to_dict(self):
		return {
			"id": self.id,
			"name": self.name,
			"email": self.email,
			"department": self.department,
			"role": self.role,
			"salary": self.salary,
			"created_at": self.created_at,
		}
