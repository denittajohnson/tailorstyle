from odoo import models, fields, api
from odoo.exceptions import ValidationError
class TailorUser(models.Model):
    _name = "tailorstyle.user"
    _description = "TailorStyle User Details"

    user_id = fields.Char(string="User ID", required=True, copy=False, readonly=True, default=lambda self: self.env['ir.sequence'].next_by_code('tailorstyle.user'))
    name = fields.Char(string="Name", required=True)
    place = fields.Char(string="Place")
    phone = fields.Char(string="Phone Number", required=True)
    password = fields.Char(string="Password", required=True, password=True)
    total_orders = fields.Integer(string="Total Orders", compute="_compute_total_orders", store=True)

    order_ids = fields.One2many("tailorstyle.order", "user_id", string="Orders")

    @api.depends("order_ids.status")
    def _compute_total_orders(self):
        for user in self:
            completed_orders = user.order_ids.filtered(lambda o: o.status == 'done')
            user.total_orders = len(completed_orders)
            
    @api.constrains('phone')
    def check_phone_number(self):
        for user in self:
            if not user.phone.isdigit() or len(user.phone) != 10:
                raise ValidationError('Phone number must have exactly 10 digits')