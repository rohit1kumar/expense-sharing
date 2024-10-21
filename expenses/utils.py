import csv
from django.http import HttpResponse
from datetime import datetime


def generate_csv(to_receive_splits, to_pay_splits, balance_summary):
    """Generate a CSV file for balance sheet data."""
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
        "Amount",
    ]
    writer.writerow(headers)

    # Write to receive splits
    for split in to_receive_splits:
        writer.writerow(
            [
                split.expense.created_at.strftime("%Y-%m-%d %I:%M %p"),
                split.expense.id,
                split.expense.title,
                "Receive From",
                split.user.email,
                split.user.name,
                split.amount,
            ]
        )

    # Write to pay splits
    for split in to_pay_splits:
        writer.writerow(
            [
                split.expense.created_at.strftime("%Y-%m-%d %I:%M %p"),
                split.expense.id,
                split.expense.title,
                "Pay To",
                split.expense.paid_by.email,
                split.expense.paid_by.name,
                split.amount,
            ]
        )

    # Write summary
    writer.writerow([])  # Empty row
    writer.writerow(
        [
            "",
            "",
            "",
            "",
            "",
            "Total Amount to Receive",
            balance_summary["to_receive"],
        ]
    )
    writer.writerow(
        [
            "",
            "",
            "",
            "",
            "",
            "Total Amount to Pay",
            balance_summary["to_pay"],
        ]
    )
    writer.writerow(
        [
            "",
            "",
            "",
            "",
            "",
            "Net Balance",
            balance_summary["net_balance"],
        ]
    )

    return response
