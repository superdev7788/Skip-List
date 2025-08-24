import random
from typing import Optional, Any, List, Tuple


class SkipListNode:
    """Node in the skip list containing key-value pair and forward pointers"""

    def __init__(self, key: Any, value: Any, level: int):
        self.key = key
        self.value = value
        self.forward = [None] * (level + 1)  # Array of forward pointers


class SkipList:
    """
    Skip List data structure implementation

    A skip list is a probabilistic data structure that allows O(log n) search complexity.
    It maintains multiple levels where higher levels act as "express lanes" for faster traversal.
    """

    def __init__(self, max_level: int = 16, probability: float = 0.5):
        """
        Initialize skip list

        Args:
            max_level: Maximum number of levels in the skip list
            probability: Probability for promoting nodes to higher levels
        """
        self.max_level = max_level
        self.probability = probability
        self.level = 0  # Current level of skip list

        # Create header node with negative infinity key
        self.header = SkipListNode(float('-inf'), None, max_level)

    def random_level(self) -> int:
        """Generate random level for new node based on probability"""
        level = 0
        while random.random() < self.probability and level < self.max_level:
            level += 1
        return level

    def search(self, key: Any) -> Optional[Any]:
        """
        Search for a key in the skip list

        Args:
            key: Key to search for

        Returns:
            Value associated with the key, or None if not found

        Time Complexity: O(log n) average case
        """
        current = self.header

        # Start from highest level and work down
        for i in range(self.level, -1, -1):
            # Move forward while key is greater than next node's key
            while (current.forward[i] is not None and
                   current.forward[i].key < key):
                current = current.forward[i]

        # Move to next node at level 0
        current = current.forward[0]

        # Check if we found the key
        if current is not None and current.key == key:
            return current.value
        return None

    def insert(self, key: Any, value: Any) -> None:
        """
        Insert a key-value pair into the skip list

        Args:
            key: Key to insert
            value: Value to associate with the key

        Time Complexity: O(log n) average case
        """
        update = [None] * (self.max_level + 1)
        current = self.header

        # Find position to insert by tracking update pointers
        for i in range(self.level, -1, -1):
            while (current.forward[i] is not None and
                   current.forward[i].key < key):
                current = current.forward[i]
            update[i] = current

        current = current.forward[0]

        # If key already exists, update value
        if current is not None and current.key == key:
            current.value = value
            return

        # Generate random level for new node
        new_level = self.random_level()

        # If new level is higher than current level, update header pointers
        if new_level > self.level:
            for i in range(self.level + 1, new_level + 1):
                update[i] = self.header
            self.level = new_level

        # Create new node
        new_node = SkipListNode(key, value, new_level)

        # Update forward pointers
        for i in range(new_level + 1):
            new_node.forward[i] = update[i].forward[i]
            update[i].forward[i] = new_node

    def delete(self, key: Any) -> bool:
        """
        Delete a key from the skip list

        Args:
            key: Key to delete

        Returns:
            True if key was found and deleted, False otherwise

        Time Complexity: O(log n) average case
        """
        update = [None] * (self.max_level + 1)
        current = self.header

        # Find the node to delete
        for i in range(self.level, -1, -1):
            while (current.forward[i] is not None and
                   current.forward[i].key < key):
                current = current.forward[i]
            update[i] = current

        current = current.forward[0]

        # If key found, delete it
        if current is not None and current.key == key:
            # Update forward pointers
            for i in range(self.level + 1):
                if update[i].forward[i] != current:
                    break
                update[i].forward[i] = current.forward[i]

            # Update skip list level
            while self.level > 0 and self.header.forward[self.level] is None:
                self.level -= 1

            return True
        return False

    def display(self) -> None:
        """Display the skip list structure level by level"""
        print("Skip List Structure:")
        for i in range(self.level, -1, -1):
            print(f"Level {i}: ", end="")
            node = self.header.forward[i]
            while node is not None:
                print(f"({node.key}, {node.value}) ", end="")
                node = node.forward[i]
            print()

    def to_list(self) -> List[Tuple[Any, Any]]:
        """Convert skip list to a list of (key, value) tuples"""
        result = []
        current = self.header.forward[0]
        while current is not None:
            result.append((current.key, current.value))
            current = current.forward[0]
        return result

    def size(self) -> int:
        """Get the number of elements in the skip list"""
        count = 0
        current = self.header.forward[0]
        while current is not None:
            count += 1
            current = current.forward[0]
        return count


# Practical Example: Employee Database Management System
class EmployeeDatabase:
    """
    Example usage of Skip List for managing employee records
    Demonstrates practical application in a database-like scenario
    """

    def __init__(self):
        # Skip list indexed by employee ID for fast lookups
        self.employees = SkipList()
        # Secondary index by salary for range queries (simplified example)
        self.salary_index = SkipList()

    def add_employee(self, emp_id: int, name: str, department: str, salary: float):
        """Add new employee to the database"""
        employee_data = {
            'name': name,
            'department': department,
            'salary': salary
        }

        self.employees.insert(emp_id, employee_data)
        # Add to salary index (in real implementation, would handle duplicates)
        self.salary_index.insert(salary, emp_id)
        print(f"Added employee: {name} (ID: {emp_id})")

    def get_employee(self, emp_id: int) -> Optional[dict]:
        """Retrieve employee by ID"""
        return self.employees.search(emp_id)

    def update_salary(self, emp_id: int, new_salary: float) -> bool:
        """Update employee salary"""
        employee = self.employees.search(emp_id)
        if employee:
            old_salary = employee['salary']
            employee['salary'] = new_salary

            # Update salary index
            self.salary_index.delete(old_salary)
            self.salary_index.insert(new_salary, emp_id)
            return True
        return False

    def remove_employee(self, emp_id: int) -> bool:
        """Remove employee from database"""
        employee = self.employees.search(emp_id)
        if employee:
            # Remove from both indexes
            self.salary_index.delete(employee['salary'])
            return self.employees.delete(emp_id)
        return False

    def list_all_employees(self) -> List[Tuple[int, dict]]:
        """List all employees sorted by ID"""
        return self.employees.to_list()

    def display_structure(self):
        """Display the internal skip list structure"""
        print("\nEmployee Database Structure:")
        self.employees.display()


# Example usage and demonstration
if __name__ == "__main__":
    print("=== Skip List Implementation Demo ===\n")

    # Basic Skip List Operations
    print("1. Basic Skip List Operations:")
    skip_list = SkipList()

    # Insert some values
    values = [(10, "Apple"), (20, "Banana"), (5, "Cherry"),
              (30, "Date"), (15, "Elderberry"), (25, "Fig")]

    for key, value in values:
        skip_list.insert(key, value)
        print(f"Inserted: {key} -> {value}")

    print(f"\nSkip list size: {skip_list.size()}")
    print("Contents:", skip_list.to_list())

    # Search operations
    print("\n2. Search Operations:")
    test_keys = [15, 25, 35]
    for key in test_keys:
        result = skip_list.search(key)
        print(f"Search {key}: {'Found - ' + result if result else 'Not found'}")

    # Display structure
    print("\n3. Skip List Structure:")
    skip_list.display()

    # Delete operations
    print("\n4. Delete Operations:")
    delete_keys = [20, 35, 5]
    for key in delete_keys:
        success = skip_list.delete(key)
        print(f"Delete {key}: {'Success' if success else 'Not found'}")

    print("After deletions:", skip_list.to_list())

    # Practical Example: Employee Database
    print("\n" + "=" * 50)
    print("5. Practical Example: Employee Database")
    print("=" * 50)

    db = EmployeeDatabase()

    # Add employees
    employees = [
        (1001, "Alice Johnson", "Engineering", 95000),
        (1005, "Bob Smith", "Marketing", 65000),
        (1002, "Carol Williams", "Engineering", 105000),
        (1008, "David Brown", "Sales", 55000),
        (1003, "Eve Davis", "HR", 70000),
        (1010, "Frank Miller", "Engineering", 120000)
    ]

    for emp_id, name, dept, salary in employees:
        db.add_employee(emp_id, name, dept, salary)

    print(f"\nTotal employees: {db.employees.size()}")

    # Retrieve specific employee
    print("\nRetrieving employee 1002:")
    emp = db.get_employee(1002)
    if emp:
        print(f"Name: {emp['name']}, Department: {emp['department']}, Salary: ${emp['salary']:,}")

    # Update salary
    print("\nUpdating Alice Johnson's salary...")
    db.update_salary(1001, 98000)
    updated_emp = db.get_employee(1001)
    print(f"New salary: ${updated_emp['salary']:,}")

    # List all employees (sorted by ID due to skip list ordering)
    print("\nAll employees (sorted by ID):")
    for emp_id, emp_data in db.list_all_employees():
        print(f"ID: {emp_id:4d} | {emp_data['name']:15s} | "
              f"{emp_data['department']:12s} | ${emp_data['salary']:,}")

    # Remove an employee
    print(f"\nRemoving employee 1008...")
    db.remove_employee(1008)
    print(f"Remaining employees: {db.employees.size()}")

    # Display internal structure
    db.display_structure()

    print("\n=== Performance Characteristics ===")
    print("Skip List provides:")
    print("• Average O(log n) search, insert, and delete operations")
    print("• Ordered traversal in O(n) time")
    print("• Space complexity: O(n) on average")
    print("• Probabilistic balancing (no complex rebalancing needed)")
    print("• Excellent for concurrent access (compared to balanced trees)")
