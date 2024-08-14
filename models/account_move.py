from odoo import fields, models, api


class AccountMove(models.Model):
    _inherit = "account.move"

    account_desired_line_ids = fields.One2many(
        "account.desired.line",
        "account_desired_id",
        string="Invoice Desired Products"
    )

    account_desired_grand_price_total = fields.Float(
        string="Total",
        compute="_compute_account_desired_grand_total",
        exportable=False
    )

    @api.depends(
        "account_desired_line_ids.account_desired_product_id",
        "account_desired_line_ids.account_desired_quantity",
        "account_desired_line_ids.account_desired_price_unit",
        "account_desired_line_ids.account_desired_price_total"
    )
    def _compute_account_desired_grand_total(self):
        for order in self:
            order.account_desired_grand_price_total = sum(
                order.account_desired_line_ids.mapped('account_desired_price_total')
            )