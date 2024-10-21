from rest_framework.decorators import action
from rest_framework import viewsets, permissions
from rest_framework.response import Response

from .models import Expense
from .serializers import ExpenseSerializer
from .services import ExpenseBalanceService
from .utils import generate_csv


class ExpenseView(viewsets.ModelViewSet):
    serializer_class = ExpenseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Expense.objects.filter(paid_by=self.request.user)

    @action(detail=False, methods=["get"], url_path="my-expenses")
    def my_expenses(self, request):
        """Get user's balance summary and split details"""
        balance_service = ExpenseBalanceService(request.user)
        return Response(balance_service.get_formatted_expense_data())

    @action(detail=False, methods=["get"], url_path="overall-expenses")
    def overall_expenses(self, request):
        """Get overall balance summary for all users"""
        user_balance = ExpenseBalanceService(request.user)
        return Response(user_balance.get_user_balance_summary())

    @action(detail=False, methods=["get"], url_path="download-balance-sheet")
    def download_balance_sheet(self, request):
        """Download balance sheet as CSV"""
        balance_service = ExpenseBalanceService(request.user)
        to_receive_splits, to_pay_splits = balance_service.get_detailed_splits()
        balance_summary = balance_service.get_user_balance_summary()
        return generate_csv(to_receive_splits, to_pay_splits, balance_summary)
