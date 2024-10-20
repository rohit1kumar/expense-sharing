from .models import Expense, ExpenseSplit
from rest_framework import serializers
from users.serializers import UserSerializer


class ExpenseSplitSerializer(serializers.ModelSerializer):
    # user = UserSerializer()

    class Meta:
        model = ExpenseSplit
        fields = ("user", "amount", "percentage")


class ExpenseSerializer(serializers.ModelSerializer):
    splits = ExpenseSplitSerializer(many=True)
    paid_by = UserSerializer(read_only=True, required=False)

    class Meta:
        model = Expense
        fields = (
            "id",
            "title",
            "description",
            "total_amount",
            "paid_by",
            "split_type",
            "splits",
            "created_at",
        )

    def validate(self, data):
        """
        validate expense type,
        if split type is percentage then sum of all percentage should be 100
        if split type is exact then sum of all split amount should be equal to total amount
        """

        split_type = data["split_type"]
        splits = data["splits"]
        total_amount = data["total_amount"]

        # Ensure logged-in user is included in splits
        user_ids = [split["user"].id for split in splits]
        if self.context["request"].user.id not in user_ids:
            raise serializers.ValidationError("Add logged-in user in splits list")

        if split_type == "PERCENTAGE":
            # Convert percentages to amounts
            total_percentage = sum(split.get("percentage", 0) for split in splits)
            if total_percentage != 100:
                raise serializers.ValidationError("Percentages must sum to 100")

            # Convert percentages to amounts in splits_data
            for split in splits:
                percentage = split.get("percentage", 0)
                split["amount"] = (total_amount * percentage) / 100

        elif split_type == "EXACT":
            total_split_amount = sum(
                split["amount"] for split in splits if split.get("amount")
            )
            if total_split_amount != total_amount:
                raise serializers.ValidationError(
                    f"Total split amount {total_split_amount} must be equal to total amount {total_amount}"
                )

        else:
            # Split type is EQUAL
            split_amount = total_amount / len(splits)
            for split in splits:
                split["amount"] = split_amount

        return data

    def create(self, validated_data):
        splits_data = validated_data.pop("splits")
        expense = Expense.objects.create(
            **validated_data, paid_by=self.context["request"].user
        )

        # bulk create expense splits
        expense_splits = []
        for split_data in splits_data:
            expense_splits.append(ExpenseSplit(expense=expense, **split_data))
        ExpenseSplit.objects.bulk_create(expense_splits)
        return expense
