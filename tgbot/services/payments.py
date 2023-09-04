from aiogram.types import LabeledPrice


class PaymentsManager:

    def __init__(self, tg_user_id: int, payment_group_id: int,
                 product_name: str, product_title: str,
                 amount: int | float, limitation_days: int,
                 percent_discount: int = 20,
                 extra_payload: str | None = None):
        self.tg_user_id = tg_user_id
        self.payment_group_id = payment_group_id
        self.product_name = product_name
        self.product_title = product_title
        self.amount = amount * 100
        self.limitation_days = limitation_days
        self.percent_discount = percent_discount
        self.extra_payload = extra_payload

    @property
    def payload(self) -> str:
        payload_data = [
            self.tg_user_id.__str__(),
            self.payment_group_id.__str__(),
            self.amount.__str__(),
            self.limitation_days.__str__(),
        ]
        if self.extra_payload:
            payload_data.append(self.extra_payload)
        return '__'.join(payload_data)

    def calc_price(self, mul: int) -> int:
        discount_sum = (self.amount // 100) * self.percent_discount
        return (self.amount - discount_sum) * mul

    @staticmethod
    def calc_price_with_discount(amount: int,
                                 percent_discount: int = 20) -> int:
        discount_sum = (amount // 100) * percent_discount
        return amount - discount_sum
