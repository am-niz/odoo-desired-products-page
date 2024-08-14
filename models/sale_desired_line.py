from odoo import fields, models, api


class SaleDesiredLine(models.Model):
    _name = "sale.desired.line"
    _description = "Sale Desired Products"

    desired_id = fields.Many2one("sale.order", string="Desired Reference")

    desired_product_id = fields.Many2one(
        string="Product",
        comodel_name='product.product',
        domain=[('sale_ok', '=', True)],
        change_default=True, ondelete='restrict',
        store=True
    )
    # previously related='product_id.product_tmpl_id'
    # not anymore since the field must be considered editable for product configurator logic
    # without modifying the related product_id when updated.

    desired_quantity = fields.Float(
        string="Quantity",
        digits='Product Unit of Measure',
        require=True,
        store=True,
        default=1.0
    )
    desired_price_unit = fields.Float(
        string="Sales Price",
        digits='Product Price',
        store=True
    )
    desired_price_total = fields.Float(
        string="Price Total",
        compute="_compute_amount",
        store=True,
        precompute=True
    )

    @api.onchange('desired_product_id')
    def _onchange_desired_product_id(self):
        if not self.desired_product_id:
            return
        self.desired_price_unit = self.desired_product_id.product_tmpl_id.list_price

    @api.depends("desired_product_id", "desired_quantity", "desired_price_unit")
    def _compute_amount(self):
        for line in self:
            line.desired_price_total = line.desired_quantity * line.desired_price_unit

