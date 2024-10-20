import csv
from rest_framework.decorators import action
from rest_framework import viewsets, permissions
from .models import Expense, ExpenseSplit, User
from .serializers import ExpenseSerializer
from django.db import models
from rest_framework.response import Response
from django.http import HttpResponse
from collections import defaultdict
from decimal import Decimal
from datetime import datetime


class ExpenseView(viewsets.ModelViewSet):
    serializer_class = ExpenseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Expense.objects.filter(paid_by=self.request.user)

    @action(detail=False, methods=["get"], url_path="download-balance-sheet")
    def download_balance_sheet(self, request):
        """Download balance sheet as CSV"""

        to_receive_splits = (
            ExpenseSplit.objects.select_related(
                "expense",
                "user",
                "expense__paid_by",
            )
            .filter(expense__paid_by=request.user)
            .exclude(user=request.user)
        )

        to_pay_splits = (
            ExpenseSplit.objects.select_related(
                "expense",
                "expense__paid_by",
                "user",
            )
            .filter(user=request.user)
            .exclude(expense__paid_by=request.user)
        )

        # Calculate totals to receive and to pay
        total_to_receive = to_receive_splits.aggregate(
            total=models.Sum("amount", output_field=models.DecimalField())
        )["total"] or Decimal("0.00")

        total_to_pay = to_pay_splits.aggregate(
            total=models.Sum("amount", output_field=models.DecimalField())
        )["total"] or Decimal("0.00")

        # Generate CSV
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = (
            f'attachment; filename="balance_sheet_{datetime.now().strftime("%Y%m%d")}.csv"'
        )
        writer = csv.writer(response)

        # Write headers
        headers = [
            "Date",
            "Transaction ID",
            "Title",
            "Type",
            "User's Email",
            "User's Name",
            "User's Mobile Number",
            "Amount",
        ]
        writer.writerow(headers)

        for split in to_receive_splits:
            writer.writerow(
                [
                    split.expense.created_at.strftime("%Y-%m-%d %I:%M %p"),
                    split.expense.id,
                    split.expense.title,
                    "To Receive",
                    split.user.email,
                    split.user.name,
                    split.user.mobile_number,
                    split.amount,
                ]
            )

        for split in to_pay_splits:
            writer.writerow(
                [
                    split.expense.created_at.strftime("%Y-%m-%d %I:%M %p"),
                    split.expense.id,
                    split.expense.title,
                    "To Pay",
                    split.expense.paid_by.email,
                    split.expense.paid_by.name,
                    split.expense.paid_by.mobile_number,
                    split.amount,
                ]
            )

        writer.writerow([])  # Empty row
        writer.writerow(
            [
                "",
                "",
                "",
                "",
                "",
                "",
                "Total Amount to Receive",
                total_to_receive,
            ]
        )
        writer.writerow(
            [
                "",
                "",
                "",
                "",
                "",
                "",
                "Total Amount to Pay",
                total_to_pay,
            ]
        )

        return response
