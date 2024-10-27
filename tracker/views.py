from django.shortcuts import render, redirect
from .forms import BudgetForm
from .models import Expense

# View to reset the budget by clearing all expenses
def reset_budget(request):
    if request.method == 'POST':
        Expense.objects.all().delete()  # Clear all the expenses
        return redirect('budget')

# Main budget view
def budget_view(request):
    # Default initial budget value
    initial_budget = 1000.00

    # Initialize total credits and total expenses
    total_credits = 0
    total_expenses = 0

    if request.method == 'POST':
        form = BudgetForm(request.POST)
        if form.is_valid():
            # Get the total budget from the form or use the initial value
            total_budget = form.cleaned_data.get('total_budget', initial_budget)
            transaction_name = form.cleaned_data['transaction_name']
            transaction_amount = form.cleaned_data['transaction_amount']

            # Get the action type: 'credit' or 'debit'
            action = request.POST.get('action')

            # Handle credit transactions
            if action == 'credit' and transaction_name and transaction_amount:
                Expense.objects.create(name=transaction_name, amount=transaction_amount)
                total_credits += transaction_amount

            # Handle debit transactions (expenses)
            elif action == 'debit' and transaction_name and transaction_amount:
                Expense.objects.create(name=transaction_name, amount=-transaction_amount)
                total_expenses += transaction_amount

            # Calculate total expenses, total credits, and remaining budget
            expenses = Expense.objects.all()
            total_expenses = sum(expense.amount for expense in expenses if expense.amount < 0)
            total_credits = sum(expense.amount for expense in expenses if expense.amount > 0)
            remaining_budget = total_budget + total_credits + total_expenses

            return render(request, 'tracker/budget.html', {
                'form': form,
                'expenses': expenses,
                'total_expenses': abs(total_expenses),
                'total_credits': total_credits,
                'remaining_budget': remaining_budget,
                'total_budget': total_budget,
                'summary': generate_trip_summary(expenses, total_budget, total_credits, total_expenses)
            })
    else:
        form = BudgetForm()

    # Initial calculation for when the form is not submitted (on GET request)
    expenses = Expense.objects.all()
    total_expenses = sum(expense.amount for expense in expenses if expense.amount < 0)
    total_credits = sum(expense.amount for expense in expenses if expense.amount > 0)
    total_budget = initial_budget  # Set the total budget to the default value
    remaining_budget = total_budget + total_credits + total_expenses

    return render(request, 'tracker/budget.html', {
        'form': form,
        'expenses': expenses,
        'total_expenses': abs(total_expenses),
        'total_credits': total_credits,
        'remaining_budget': remaining_budget,
        'total_budget': total_budget,
        'summary': generate_trip_summary(expenses, total_budget, total_credits, total_expenses)
    })

# Helper function to generate the trip summary
def generate_trip_summary(expenses, total_budget, total_credits, total_expenses):
    summary = {
        'total_budget': total_budget,
        'total_credits': total_credits,
        'total_expenses': abs(total_expenses),
        'remaining_budget': total_budget + total_credits + total_expenses,
        'transactions': []
    }

    for expense in expenses:
        summary['transactions'].append({
            'name': expense.name,
            'amount': expense.amount,
            'type': 'Credit' if expense.amount > 0 else 'Debit'
        })
    
    return summary
