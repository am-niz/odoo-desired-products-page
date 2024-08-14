from odoo import fields, models, api


class AccountDesiredLine(models.Model):
    _name = "account.desired.line"
    _description = "Account Desired Products"

    account_desired_id = fields.Many2one("account.move", string="Desired Reference")
    account_desired_product_id = fields.Many2one(
        string="Product",
        comodel_name='product.product',
        store=True
    )
    # previously related='product_id.product_tmpl_id'
    # not anymore since the field must be considered editable for product configurator logic
    # without modifying the related product_id when updated.

    account_desired_quantity = fields.Float(
        string="Quantity",
        digits='Product Unit of Measure',
        require=True,
        store=True,
        default=1.0
    )
    account_desired_price_unit = fields.Float(
        string="Sales Price",
        digits='Product Price',
        store=True
    )
    account_desired_price_total = fields.Float(
        string="Price Total",
        compute="_compute_account_desired_price_total",
        store=True,
        precompute=True
    )

    @api.onchange('account_desired_product_id')
    def _onchange_account_desired_product_id(self):
        if not self.account_desired_product_id:
            return
        self.account_desired_price_unit = self.account_desired_product_id.product_tmpl_id.list_price

    @api.depends("account_desired_product_id", "account_desired_quantity", "account_desired_price_unit")
    def _compute_account_desired_price_total(self):
        for line in self:
            line.account_desired_price_total = line.account_desired_quantity * line.account_desired_price_unit
