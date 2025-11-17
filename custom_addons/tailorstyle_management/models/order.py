from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import date

class TailorOrder(models.Model):
    _name = "tailorstyle.order"
    _description = "Order Details"
    _rec_name = "order_id"

    order_id = fields.Char(string="Order ID", required=True, copy=False, readonly=True, default=lambda self: self.env['ir.sequence'].next_by_code('tailorstyle.order'))
    user_id = fields.Many2one("tailorstyle.user", string="User ID", required=True)
    user_code = fields.Char(string="User ID", related="user_id.user_id", store=True, readonly=True)
    cloth_id = fields.Many2one("tailorstyle.cloth", string="Cloth", required=True)
    cloth_code = fields.Char(related="cloth_id.cloth_code", string="Cloth ID", store=True, readonly=True)
    customer_name = fields.Char(related="user_id.name", string="Name", store=True)
    phone = fields.Char(related="user_id.phone", string="Phone", store=True)
    place = fields.Char(related="user_id.place", string="Place", store=True)
    date_of_order = fields.Datetime(string="Order Placed", default=fields.Datetime.now)
    is_urgent = fields.Boolean(string="Is Urgent?", readonly="True")
    urgent_date = fields.Date(string="Date", readonly="True")
    status = fields.Selection([
        ('ordered', 'Ordered'),
        ('processing', 'Processing'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled'),
    ], string="Status", default="ordered")

    price = fields.Float(related="cloth_id.price", string="Price", store=True)
    bubbled = fields.Selection([
        ('nighty', 'Nighty'),
        ('nightdress', 'Night Dress'),
        ('frocknighty', 'Frock Nighty'),
        ('churidar', 'Churidar'),
        ('others', 'Others'),
    ], string="Bubbled Option", store=True)
    cloth_image = fields.Binary(related="cloth_id.main_image", string="Image", store=True)

    @api.constrains('urgent_date', 'date_of_order')
    def _check_urgent_date(self):
        for rec in self:
            if rec.is_urgent and rec.urgent_date:
                # compare dates (date_of_order is datetime)
                order_dt = fields.Datetime.context_timestamp(rec, rec.date_of_order).date() if rec.date_of_order else date.today()
                if rec.urgent_date < order_dt:
                    raise ValidationError("Urgent date cannot be earlier than order placed date.")

    @api.model
    def create(self, vals):
        record = super(TailorOrder, self).create(vals)
        if record.cloth_id:
            cloth = record.cloth_id.sudo()
            new_stock = max((cloth.stock or 0) - 1, 0)
            cloth.write({'stock': new_stock})
        return record

    def write(self, vals):
        # handle cancellation stock restore: only when changing INTO cancelled from a different state
        for order in self:
            if 'status' in vals:
                new_status = vals.get('status')
                old_status = order.status
                # If the new status is 'cancelled' and previously it was not 'cancelled',
                # then increase stock once.
                if new_status == 'cancelled' and old_status != 'cancelled':
                    if order.cloth_id:
                        cloth = order.cloth_id.sudo()
                        cloth.write({'stock': (cloth.stock or 0) + 1})
        
    
        result = super(TailorOrder, self).write(vals)

        # If status changed → recompute user's total orders
        if 'status' in vals:
            for order in self:
                if order.user_id:
                    order.user_id._compute_total_orders()

        return result
