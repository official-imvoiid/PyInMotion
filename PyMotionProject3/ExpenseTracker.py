import os
import json
from datetime import datetime
import calendar
from typing import Dict, List, Any, Optional, Tuple


class ExpenseTracker:
    """
    Expense Tracker application that allows users to track and analyze their daily expenses.
    """
    
    def __init__(self, data_file: str = "expenses.json"):
        """
        Initialize the Expense Tracker with a data file.
        
        Args:
            data_file: The file path to store expense data
        """
        self.data_file = data_file
        self.categories = [
            "Food", "Transportation", "Housing", "Entertainment", 
            "Shopping", "Utilities", "Healthcare", "Education", "Other"
        ]
        self.expenses = self._load_data()
        
    def _load_data(self) -> List[Dict[str, Any]]:
        """Load expense data from the data file."""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as file:
                    return json.load(file)
            except json.JSONDecodeError:
                print("Error: Data file is corrupted. Starting with empty data.")
                return []
        return []
    
    def _save_data(self) -> None:
        """Save expense data to the data file."""
        try:
            with open(self.data_file, 'w') as file:
                json.dump(self.expenses, file, indent=4)
        except Exception as e:
            print(f"Error saving data: {e}")
    
    def add_expense(self, amount: float, description: str, category: str, date: Optional[str] = None) -> bool:
        """
        Add a new expense to the tracker.
        
        Args:
            amount: The expense amount
            description: A brief description of the expense
            category: The expense category
            date: The date of the expense (defaults to today if None)
            
        Returns:
            bool: True if the expense was added successfully, False otherwise
        """
        # Input validation
        try:
            amount = float(amount)
            if amount <= 0:
                print("Error: Amount must be greater than zero.")
                return False
                
            if category not in self.categories:
                print(f"Error: Category must be one of: {', '.join(self.categories)}")
                return False
                
            # Use today's date if none provided
            if date is None:
                date = datetime.now().strftime("%Y-%m-%d")
            else:
                # Validate date format
                datetime.strptime(date, "%Y-%m-%d")
                
            # Create expense record
            expense = {
                "id": len(self.expenses) + 1,
                "amount": amount,
                "description": description,
                "category": category,
                "date": date,
                "timestamp": datetime.now().isoformat()
            }
            
            self.expenses.append(expense)
            self._save_data()
            print(f"Expense of ${amount:.2f} added successfully.")
            return True
            
        except ValueError as e:
            print(f"Error: {e}")
            return False
    
    def delete_expense(self, expense_id: int) -> bool:
        """
        Delete an expense by its ID.
        
        Args:
            expense_id: The ID of the expense to delete
            
        Returns:
            bool: True if the expense was deleted, False otherwise
        """
        for i, expense in enumerate(self.expenses):
            if expense["id"] == expense_id:
                del self.expenses[i]
                self._save_data()
                print(f"Expense with ID {expense_id} deleted successfully.")
                return True
                
        print(f"Error: No expense found with ID {expense_id}.")
        return False
    
    def edit_expense(self, expense_id: int, **kwargs) -> bool:
        """
        Edit an existing expense.
        
        Args:
            expense_id: The ID of the expense to edit
            **kwargs: Fields to update (amount, description, category, date)
            
        Returns:
            bool: True if the expense was updated, False otherwise
        """
        for expense in self.expenses:
            if expense["id"] == expense_id:
                # Validate and update fields
                try:
                    if "amount" in kwargs:
                        amount = float(kwargs["amount"])
                        if amount <= 0:
                            print("Error: Amount must be greater than zero.")
                            return False
                        expense["amount"] = amount
                        
                    if "category" in kwargs and kwargs["category"] in self.categories:
                        expense["category"] = kwargs["category"]
                    elif "category" in kwargs:
                        print(f"Error: Category must be one of: {', '.join(self.categories)}")
                        return False
                        
                    if "description" in kwargs:
                        expense["description"] = kwargs["description"]
                        
                    if "date" in kwargs:
                        # Validate date format
                        datetime.strptime(kwargs["date"], "%Y-%m-%d")
                        expense["date"] = kwargs["date"]
                        
                    # Update timestamp
                    expense["timestamp"] = datetime.now().isoformat()
                    self._save_data()
                    print(f"Expense with ID {expense_id} updated successfully.")
                    return True
                    
                except ValueError as e:
                    print(f"Error: {e}")
                    return False
                    
        print(f"Error: No expense found with ID {expense_id}.")
        return False
    
    def get_all_expenses(self) -> List[Dict[str, Any]]:
        """Get all expenses."""
        return self.expenses
    
    def get_expenses_by_category(self, category: str) -> List[Dict[str, Any]]:
        """
        Get all expenses in a specific category.
        
        Args:
            category: The category to filter by
            
        Returns:
            List of expenses in the specified category
        """
        if category not in self.categories:
            print(f"Error: Category must be one of: {', '.join(self.categories)}")
            return []
            
        return [e for e in self.expenses if e["category"] == category]
    
    def get_expenses_by_date_range(self, start_date: str, end_date: str) -> List[Dict[str, Any]]:
        """
        Get expenses within a date range.
        
        Args:
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
            
        Returns:
            List of expenses within the date range
        """
        try:
            start = datetime.strptime(start_date, "%Y-%m-%d")
            end = datetime.strptime(end_date, "%Y-%m-%d")
            
            return [
                e for e in self.expenses 
                if start <= datetime.strptime(e["date"], "%Y-%m-%d") <= end
            ]
        except ValueError as e:
            print(f"Error: {e}")
            return []
    
    def get_monthly_summary(self, year: int, month: int) -> Dict[str, Any]:
        """
        Get a summary of expenses for a specific month.
        
        Args:
            year: The year
            month: The month (1-12)
            
        Returns:
            Dictionary with monthly summary data
        """
        try:
            # Validate month
            if not 1 <= month <= 12:
                raise ValueError("Month must be between 1 and 12")
                
            # Create date range for the month
            last_day = calendar.monthrange(year, month)[1]
            start_date = f"{year}-{month:02d}-01"
            end_date = f"{year}-{month:02d}-{last_day:02d}"
            
            # Get expenses for the month
            monthly_expenses = self.get_expenses_by_date_range(start_date, end_date)
            
            # Calculate total
            total = sum(expense["amount"] for expense in monthly_expenses)
            
            # Calculate category breakdown
            category_totals = {}
            for category in self.categories:
                category_expenses = [e for e in monthly_expenses if e["category"] == category]
                category_total = sum(e["amount"] for e in category_expenses)
                if category_total > 0:
                    category_totals[category] = category_total
            
            # Create summary
            summary = {
                "year": year,
                "month": month,
                "month_name": calendar.month_name[month],
                "total_expenses": total,
                "num_expenses": len(monthly_expenses),
                "category_breakdown": category_totals,
                "expenses": monthly_expenses
            }
            
            return summary
            
        except ValueError as e:
            print(f"Error: {e}")
            return {}
    
    def get_annual_summary(self, year: int) -> Dict[str, Any]:
        """
        Get a summary of expenses for a specific year.
        
        Args:
            year: The year
            
        Returns:
            Dictionary with annual summary data
        """
        try:
            # Create date range for the year
            start_date = f"{year}-01-01"
            end_date = f"{year}-12-31"
            
            # Get expenses for the year
            annual_expenses = self.get_expenses_by_date_range(start_date, end_date)
            
            # Calculate total
            total = sum(expense["amount"] for expense in annual_expenses)
            
            # Calculate monthly breakdown
            monthly_totals = {}
            for month in range(1, 13):
                month_summary = self.get_monthly_summary(year, month)
                monthly_totals[calendar.month_name[month]] = month_summary["total_expenses"]
            
            # Calculate category breakdown
            category_totals = {}
            for category in self.categories:
                category_expenses = [e for e in annual_expenses if e["category"] == category]
                category_total = sum(e["amount"] for e in category_expenses)
                if category_total > 0:
                    category_totals[category] = category_total
            
            # Create summary
            summary = {
                "year": year,
                "total_expenses": total,
                "num_expenses": len(annual_expenses),
                "monthly_breakdown": monthly_totals,
                "category_breakdown": category_totals
            }
            
            return summary
            
        except ValueError as e:
            print(f"Error: {e}")
            return {}


class ExpenseTrackerUI:
    """User interface for the Expense Tracker application."""
    
    def __init__(self):
        """Initialize the UI with an ExpenseTracker instance."""
        self.tracker = ExpenseTracker()
        
    def display_menu(self) -> None:
        """Display the main menu."""
        print("\n==== EXPENSE TRACKER ====")
        print("1. Add Expense")
        print("2. View All Expenses")
        print("3. View Expenses by Category")
        print("4. View Monthly Summary")
        print("5. View Annual Summary")
        print("6. Edit Expense")
        print("7. Delete Expense")
        print("8. Exit")
        print("=========================")
    
    def get_menu_choice(self) -> int:
        """Get user's menu choice."""
        while True:
            try:
                choice = int(input("Enter your choice (1-8): "))
                if 1 <= choice <= 8:
                    return choice
                print("Please enter a number between 1 and 8.")
            except ValueError:
                print("Please enter a valid number.")
    
    def add_expense_menu(self) -> None:
        """Menu for adding a new expense."""
        print("\n== Add New Expense ==")
        try:
            amount = float(input("Amount: $"))
            description = input("Description: ")
            
            print("\nCategories:")
            for i, category in enumerate(self.tracker.categories, 1):
                print(f"{i}. {category}")
                
            category_choice = int(input("\nSelect category (1-9): "))
            if not 1 <= category_choice <= len(self.tracker.categories):
                print("Invalid category choice.")
                return
                
            category = self.tracker.categories[category_choice - 1]
            
            date_input = input("Date (YYYY-MM-DD) or leave blank for today: ")
            date = date_input if date_input else None
            
            self.tracker.add_expense(amount, description, category, date)
            
        except ValueError as e:
            print(f"Error: {e}")
    
    def view_all_expenses(self) -> None:
        """Display all expenses."""
        expenses = self.tracker.get_all_expenses()
        self._display_expenses(expenses, "All Expenses")
    
    def view_expenses_by_category(self) -> None:
        """Display expenses filtered by category."""
        print("\n== Select Category ==")
        for i, category in enumerate(self.tracker.categories, 1):
            print(f"{i}. {category}")
            
        try:
            category_choice = int(input("\nSelect category (1-9): "))
            if not 1 <= category_choice <= len(self.tracker.categories):
                print("Invalid category choice.")
                return
                
            category = self.tracker.categories[category_choice - 1]
            expenses = self.tracker.get_expenses_by_category(category)
            self._display_expenses(expenses, f"{category} Expenses")
            
        except ValueError:
            print("Please enter a valid number.")
    
    def view_monthly_summary(self) -> None:
        """Display monthly expense summary."""
        try:
            year = int(input("Enter year (YYYY): "))
            month = int(input("Enter month (1-12): "))
            
            summary = self.tracker.get_monthly_summary(year, month)
            if not summary:
                return
                
            print(f"\n== Monthly Summary: {summary['month_name']} {summary['year']} ==")
            print(f"Total Expenses: ${summary['total_expenses']:.2f}")
            print(f"Number of Expenses: {summary['num_expenses']}")
            
            if summary['category_breakdown']:
                print("\nCategory Breakdown:")
                for category, amount in sorted(
                    summary['category_breakdown'].items(), 
                    key=lambda x: x[1], 
                    reverse=True
                ):
                    percentage = (amount / summary['total_expenses']) * 100 if summary['total_expenses'] > 0 else 0
                    print(f"  {category}: ${amount:.2f} ({percentage:.1f}%)")
            
            if summary['expenses']:
                print("\nExpenses this month:")
                self._display_expenses(summary['expenses'], show_header=False)
                
        except ValueError:
            print("Please enter valid numbers for year and month.")
    
    def view_annual_summary(self) -> None:
        """Display annual expense summary."""
        try:
            year = int(input("Enter year (YYYY): "))
            
            summary = self.tracker.get_annual_summary(year)
            if not summary:
                return
                
            print(f"\n== Annual Summary: {summary['year']} ==")
            print(f"Total Expenses: ${summary['total_expenses']:.2f}")
            print(f"Number of Expenses: {summary['num_expenses']}")
            
            if summary['monthly_breakdown']:
                print("\nMonthly Breakdown:")
                for month, amount in summary['monthly_breakdown'].items():
                    if amount > 0:
                        percentage = (amount / summary['total_expenses']) * 100 if summary['total_expenses'] > 0 else 0
                        print(f"  {month}: ${amount:.2f} ({percentage:.1f}%)")
            
            if summary['category_breakdown']:
                print("\nCategory Breakdown:")
                for category, amount in sorted(
                    summary['category_breakdown'].items(), 
                    key=lambda x: x[1], 
                    reverse=True
                ):
                    percentage = (amount / summary['total_expenses']) * 100 if summary['total_expenses'] > 0 else 0
                    print(f"  {category}: ${amount:.2f} ({percentage:.1f}%)")
                
        except ValueError:
            print("Please enter a valid year.")
    
    def edit_expense_menu(self) -> None:
        """Menu for editing an expense."""
        try:
            # First, show all expenses to select from
            self.view_all_expenses()
            
            expense_id = int(input("\nEnter the ID of the expense to edit: "))
            
            # Check if expense exists
            expense_exists = any(e["id"] == expense_id for e in self.tracker.get_all_expenses())
            if not expense_exists:
                print(f"No expense found with ID {expense_id}.")
                return
            
            print("\nLeave blank to keep current value")
            
            # Get current values
            current = next(e for e in self.tracker.get_all_expenses() if e["id"] == expense_id)
            
            # Amount
            amount_input = input(f"Amount (current: ${current['amount']:.2f}): ")
            amount = float(amount_input) if amount_input else None
            
            # Description
            description = input(f"Description (current: {current['description']}): ") or None
            
            # Category
            print("\nCategories:")
            for i, category in enumerate(self.tracker.categories, 1):
                print(f"{i}. {category}")
            print(f"Current category: {current['category']}")
            
            category_input = input("Select new category (1-9) or leave blank: ")
            category = self.tracker.categories[int(category_input) - 1] if category_input else None
            
            # Date
            date = input(f"Date (YYYY-MM-DD) (current: {current['date']}): ") or None
            
            # Prepare updates
            updates = {}
            if amount is not None:
                updates["amount"] = amount
            if description is not None:
                updates["description"] = description
            if category is not None:
                updates["category"] = category
            if date is not None:
                updates["date"] = date
                
            if updates:
                self.tracker.edit_expense(expense_id, **updates)
            else:
                print("No changes made.")
                
        except (ValueError, IndexError) as e:
            print(f"Error: {e}")
    
    def delete_expense_menu(self) -> None:
        """Menu for deleting an expense."""
        try:
            # First, show all expenses to select from
            self.view_all_expenses()
            
            expense_id = int(input("\nEnter the ID of the expense to delete: "))
            
            # Confirm deletion
            confirm = input(f"Are you sure you want to delete expense #{expense_id}? (y/n): ")
            if confirm.lower() == 'y':
                self.tracker.delete_expense(expense_id)
            else:
                print("Deletion cancelled.")
                
        except ValueError:
            print("Please enter a valid expense ID.")
    
    def _display_expenses(self, expenses: List[Dict[str, Any]], title: Optional[str] = None, 
                         show_header: bool = True) -> None:
        """
        Display a list of expenses in a tabular format.
        
        Args:
            expenses: List of expense dictionaries to display
            title: Optional title to display
            show_header: Whether to show the header
        """
        if not expenses:
            print("\nNo expenses found.")
            return
            
        if title and show_header:
            print(f"\n== {title} ==")
        
        # Define column widths
        id_width = 4
        date_width = 10
        amount_width = 10
        category_width = 15
        desc_width = 30
        
        # Print header
        if show_header:
            print(f"{'ID':^{id_width}} | {'Date':^{date_width}} | {'Amount':^{amount_width}} | "
                  f"{'Category':^{category_width}} | {'Description':^{desc_width}}")
            print("-" * (id_width + date_width + amount_width + category_width + desc_width + 12))
        
        # Print expenses
        for expense in sorted(expenses, key=lambda e: e["date"], reverse=True):
            id_str = str(expense["id"])
            amount_str = f"${expense['amount']:.2f}"
            # Truncate description if too long
            desc = expense["description"]
            if len(desc) > desc_width - 3:
                desc = desc[:desc_width - 3] + "..."
                
            print(f"{id_str:^{id_width}} | {expense['date']:^{date_width}} | "
                  f"{amount_str:>{amount_width}} | {expense['category']:^{category_width}} | "
                  f"{desc:<{desc_width}}")
    
    def run(self) -> None:
        """Run the Expense Tracker application."""
        print("Welcome to Expense Tracker!")
        
        while True:
            self.display_menu()
            choice = self.get_menu_choice()
            
            if choice == 1:
                self.add_expense_menu()
            elif choice == 2:
                self.view_all_expenses()
            elif choice == 3:
                self.view_expenses_by_category()
            elif choice == 4:
                self.view_monthly_summary()
            elif choice == 5:
                self.view_annual_summary()
            elif choice == 6:
                self.edit_expense_menu()
            elif choice == 7:
                self.delete_expense_menu()
            elif choice == 8:
                print("\nThank you for using Expense Tracker. Goodbye!")
                break


if __name__ == "__main__":
    # Run the application
    app = ExpenseTrackerUI()
    app.run()