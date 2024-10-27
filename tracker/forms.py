from django import forms

class BudgetForm(forms.Form):
    total_budget = forms.DecimalField(label='Total Budget', max_digits=10, decimal_places=2, initial=1000.00)
    transaction_name = forms.CharField(label='Transaction Name', max_length=100, required=False)
    transaction_amount = forms.DecimalField(label='Amount', max_digits=10, decimal_places=2, required=False)
