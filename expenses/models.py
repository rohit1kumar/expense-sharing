from django.db import models
from users.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid
from decimal import Decimal


class Expense(models.Model):
    SPLIT_CHOICES = (
        ("EQUAL", "equal"),
        ("EXACT", "exact"),
        ("PERCENTAGE", "percentage"),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    total_amount = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal("0.00"))]
    )
    paid_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="expenses_paid"
    )
    split_type = models.CharField(max_length=10, choices=SPLIT_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "expenses"


class ExpenseSplit(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    expense = models.ForeignKey(
        Expense, on_delete=models.CASCADE, related_name="splits"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        validators=[
            MinValueValidator(Decimal("0.00")),
            MaxValueValidator(Decimal("100.00")),
        ],
    )

    class Meta:
        db_table = "expense_splits"
