from libs.utils import humanize_date
from libs import NAP_DATE_FORMAT, NAP_DIGIT_PRECISION

import os
import csv
import decimal

decimal.getcontext().rounding = decimal.ROUND_HALF_UP


def export_to_csv(list_object, csv_file, fieldnames):

    csv_list_object = humanize_date(list_object)

    with open(csv_file, "w") as fd:
        writer = csv.DictWriter(
            fd,
            fieldnames=fieldnames,
            quotechar='"',
            quoting=csv.QUOTE_ALL,
        )

        header = {fieldname: fieldname.replace("_", " ").title() for fieldname in fieldnames}
        writer.writerow(header)
        for elements in csv_list_object:
            writer.writerow(elements)


def export_statements(filename, statements):
    export_to_csv(
        statements,
        filename,
        [
            "trade_date",
            "settle_date",
            "currency",
            "activity_type",
            "symbol_description",
            "symbol",
            "quantity",
            "price",
            "amount",
        ],
    )


def export_app8_part1(filename, statements):
    export_statements = [
        {
            **{
                "count": statement["quantity"],
                "acquire_date": statement["trade_date"].strftime(NAP_DATE_FORMAT),
                "purchase_price_in_currency": statement["price"],
                "purchase_price_in_lev": (statement["price"] * statement["exchange_rate"]).quantize(
                    decimal.Decimal(NAP_DIGIT_PRECISION)
                ),
            },
            **{
                k: v
                for k, v in statement.items()
                if k
                not in [
                    "trade_date",
                    "settle_date",
                    "currency",
                    "activity_type",
                    "symbol_description",
                    "symbol",
                    "quantity",
                    "price",
                    "amount",
                    "exchange_rate_date",
                    "exchange_rate",
                ]
            },
        }
        for statement in statements
        if statement["activity_type"] == "BUY"
    ]
    export_to_csv(
        export_statements,
        filename,
        ["count", "acquire_date", "purchase_price_in_currency", "purchase_price_in_lev"],
    )


def export_app5_table2(filename, sales):
    sales = [
        {
            **{k: v for k, v in sale.items() if k not in ["symbol", "avg_purchase_price", "sell_exchange_rate"]},
            **{"code": 508},
        }
        for sale in sales
    ]
    export_to_csv(
        sales,
        filename,
        ["code", "trade_date", "sell_price", "purchase_price", "profit", "loss"],
    )


def export_app8_part4_1(filename, dividends):
    dividends = [
        {**{k: v for k, v in dividend.items() if k not in ["symbol"]}, **{"profit_code": 8141, "tax_code": 1}}
        for dividend in dividends
    ]
    export_to_csv(
        dividends,
        filename,
        ["profit_code", "tax_code", "gross_profit_amount", "paid_tax_amount"],
    )
