from odoo import fields, models, api


class SaleOrder(models.Model):
    _inherit = "sale.order"

    desired_line_ids = fields.One2many(
        "sale.desired.line",
        "desired_id",
        string="Desired Products"
    )

    desired_grand_price_total = fields.Float(
        string="Total",
        compute="_compute_desired_grand_total",
        exportable=False
    )

    @api.depends(
        "desired_line_ids.desired_product_id",
        "desired_line_ids.desired_quantity",
        "desired_line_ids.desired_price_unit",
        "desired_line_ids.desired_price_total"
    )
    def _compute_desired_grand_total(self):
        for order in self:
            order.desired_grand_price_total = sum(order.desired_line_ids.mapped('desired_price_total'))

    def _create_invoices(self, grouped=False, final=False):
        # Create the invoices using the base implementation
        invoices = super(SaleOrder, self)._create_invoices(grouped=grouped, final=final)

        for order in self:
            for invoice in invoices:
                for desired_line in order.desired_line_ids:
                    invoice_desired_vals = {
                        "account_desired_id": invoice.id,
                        "account_desired_product_id": desired_line.desired_product_id.id,
                        "account_desired_quantity": desired_line.desired_quantity,
                        "account_desired_price_unit": desired_line.desired_price_unit
                    }
                    self.env["account.desired.line"].create(invoice_desired_vals)

        return invoices

