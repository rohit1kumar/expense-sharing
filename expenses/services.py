from django.db.models import Sum
from decimal import Decimal
from .models import ExpenseSplit


class ExpenseBalanceService:
    def __init__(self, user):
        self.user = user

    def get_user_balance_summary(self):
        """Get user's to pay and to receive summary"""
        to_pay = ExpenseSplit.objects.filter(user=self.user).exclude(
            expense__paid_by=self.user
        )
        to_pay = to_pay.aggregate(total=Sum("amount"))["total"] or Decimal("0.00")

        to_receive = ExpenseSplit.objects.filter(expense__paid_by=self.user).exclude(
            user=self.user
        )
        to_receive = to_receive.aggregate(total=Sum("amount"))["total"] or Decimal(
            "0.00"
        )

        return {
            "to_pay": to_pay,
            "to_receive": to_receive,
            "net_balance": to_receive - to_pay,
        }

    def get_detailed_splits(self):
        """Get detailed to pay and to receive splits"""
        to_receive_splits = (
            ExpenseSplit.objects.select_related(
                "expense",
                "user",
                "expense__paid_by",
            )
            .filter(expense__paid_by=self.user)
            .exclude(user=self.user)
        )

        to_pay_splits = (
            ExpenseSplit.objects.select_related(
                "expense",
                "expense__paid_by",
                "user",
            )
            .filter(user=self.user)
            .exclude(expense__paid_by=self.user)
        )

        return to_receive_splits, to_pay_splits

    def get_formatted_expense_data(self):
        """Format the detailed splits and balance summary"""
        to_receive_splits, to_pay_splits = self.get_detailed_splits()
        balance_summary = self.get_user_balance_summary()

        formatted_data = {
            "balance_summary": balance_summary,
            "splits": {
                "receive_from": [
                    {
                        "date": split.expense.created_at.strftime("%Y-%m-%d %I:%M %p"),
                        "expense_id": split.expense.id,
                        "title": split.expense.title,
                        "user_email": split.user.email,
                        "user_name": split.user.name,
                        "amount": split.amount,
                    }
                    for split in to_receive_splits
                ],
                "pay_to": [
                    {
                        "date": split.expense.created_at.strftime("%Y-%m-%d %I:%M %p"),
                        "expense_id": split.expense.id,
                        "title": split.expense.title,
                        "user_email": split.expense.paid_by.email,
                        "user_name": split.expense.paid_by.name,
                        "amount": split.amount,
                    }
                    for split in to_pay_splits
                ],
            },
        }

        return formatted_data
