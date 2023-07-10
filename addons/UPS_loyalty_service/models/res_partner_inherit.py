from odoo import models,fields

class ResPartnerInherit(models.Model):
    _inherit = "res.partner"

    x_birth_date =  fields.Date(string="Fecha de Nacimiento")