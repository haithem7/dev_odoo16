# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProductProduct(models.Model):
    _inherit = 'product.product'

    last_purchase_line_ids = fields.One2many(
        comodel_name="purchase.order.line",
        inverse_name="product_id",
        domain=lambda self: [
            ("state", "in", ["purchase", "done"]),
            ("company_id", "in", self.env.companies.ids),
        ],
        string="Last Purchase Order Lines",
    )

    last_purchase_price = fields.Float(
        compute="_compute_last_purchase_line_id_info", string="Last Purchase Price"
    )
    last_purchase_line_id = fields.Many2one(
        comodel_name="purchase.order.line",
        compute="_compute_last_purchase_line_id",
        string="Last Purchase Line",
    )

    @api.depends("last_purchase_line_ids")
    def _compute_last_purchase_line_id(self):
        for item in self:
            item.last_purchase_line_id = fields.first(item.last_purchase_line_ids)

    @api.depends("last_purchase_line_id")
    def _compute_last_purchase_line_id_info(self):
        for item in self:
            item.last_purchase_price = item.last_purchase_line_id.price_unit

    @api.depends(
        "last_purchase_line_id",
        "show_last_purchase_price_currency",
        "last_purchase_currency_id",
        "last_purchase_date",
    )
    def _compute_last_purchase_price_currency(self):
        for item in self:
            if item.show_last_purchase_price_currency:
                rates = item.last_purchase_currency_id._get_rates(
                    item.last_purchase_line_id.company_id, item.last_purchase_date
                )
                item.last_purchase_price_currency = rates.get(
                    item.last_purchase_currency_id.id
                )
            else:
                item.last_purchase_price_currency = 1

    marge1 = fields.Float(
        string='Cost Margin')
    marge2 = fields.Float(
        string='Last Price Margin', )


class ProductTemplate(models.Model):
    _inherit = "product.template"

    last_purchase_line_ids = fields.One2many(
        comodel_name="purchase.order.line",
        related="product_variant_ids.last_purchase_line_ids",
        string="Last Purchase Order Lines",
    )
    last_purchase_line_id = fields.Many2one(
        comodel_name="purchase.order.line",
        compute="_compute_last_purchase_line_id",
        string="Last Purchase Line",
    )
    last_purchase_price = fields.Float(
        compute="_compute_last_purchase_line_id_info", string="Last Purchase Price"
    )

    @api.depends("last_purchase_line_ids")
    def _compute_last_purchase_line_id(self):
        for item in self:
            item.last_purchase_line_id = fields.first(item.last_purchase_line_ids)

    @api.depends("last_purchase_line_id")
    def _compute_last_purchase_line_id_info(self):
        for item in self:
            item.last_purchase_price = item.last_purchase_line_id.price_unit


class SaleOrder(models.Model):
    _inherit = 'sale.order'
    total_marge = fields.Float(
        string='Total Margin', compute='_compute_margin', store=True)

    @api.depends("order_line.marge")
    def _compute_margin(self):
        for order in self:
            order.total_marge = sum(order.mapped("order_line.marge"))


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    marge1 = fields.Float(
        string='Cost Margin', compute='_compute_marge', store=True)
    marge2 = fields.Float(
        string='Last Price Margin', compute='_compute_marge', store=True)
    marge = fields.Float(
        string='Total Margin', compute='_compute_marge', store=True)

    @api.depends('price_subtotal', 'product_uom_qty')
    def _compute_marge(self):
        for rec in self:
            if rec.product_id and rec.product_id.standard_price:
                rec.marge1 = rec.price_unit - rec.product_id.standard_price
                rec.marge2 = rec.price_unit - rec.product_id.last_purchase_price
                rec.marge = rec.marge1 - rec.marge2
