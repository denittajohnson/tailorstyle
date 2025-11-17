from odoo import models, fields, api
from odoo.exceptions import ValidationError

class TailorCloth(models.Model):
    _name = "tailorstyle.cloth"
    _description = "Cloth Details"

    cloth_code = fields.Char(string="Cloth ID", required=True, readonly=True, default=lambda self: self.env['ir.sequence'].next_by_code('tailorstyle.cloth'))
    name = fields.Char(string="Name", required=True)
    material = fields.Char(string="Material")
    price = fields.Float(string="Price", required=True)
    initial_stock = fields.Integer(string="Stock", readonly="True", default=1)
    stock = fields.Integer(string="Available Stock", default=1)
    main_image = fields.Image(string="Main Image")
    sub_image = fields.Image(string="Sub Image")
    bubbled = fields.Selection([
        ('nighty', 'Nighty'),
        ('nightdress', 'Night Dress'),
        ('frocknighty', 'Frock Nighty'),
        ('churidar', 'Churidar'),
        ('others', 'Others'),
    ], string="Bubbled Option")
    allow_bubbled_option = fields.Boolean(string="Enable", default=False)
    comments = fields.Text(string="Comments")
    
    show_in_website = fields.Boolean(string="Show in Website", default=True)

    
    
    # -------- COPY STOCK → INITIAL STOCK ONLY WHEN CREATING THE RECORD --------
    @api.model
    def create(self, vals):
        if 'stock' in vals:
            vals['initial_stock'] = vals['stock']   # copy at creation
        return super(TailorCloth, self).create(vals)

    # Update stock when an order is created or cancelled
   # @api.model
    #def reduce_stock(self, cloth_id):
        #cloth = self.browse(cloth_id)
        #if cloth.stock > 0:
            #cloth.stock -= 1

    @api.model
    def increase_stock(self, cloth_id):
        cloth = self.browse(cloth_id)
        cloth.stock += 1
        
    # to validate bubbled option
    @api.constrains('bubbled', 'allow_bubbled_option')
    def check_bubbled_option(self):
        for cloth in self:
            if not cloth.allow_bubbled_option and cloth.bubbled:
                raise ValidationError("Unchecked the enable")
            
            
            