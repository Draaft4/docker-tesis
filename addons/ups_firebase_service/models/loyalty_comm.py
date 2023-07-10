from odoo import models, api
import firebase_admin
from firebase_admin import credentials, firestore

class CustomLoyalty(models.Model):
    _inherit="loyalty.card"

    @api.model
    def write(self, vals):
        res = super(CustomLoyalty, self).write(vals)
        if not self.env.context.get('loyalty_no_mail', False) and 'points' in vals:
            points_before = {coupon: coupon.points for coupon in self}
        if not self.env.context.get('loyalty_no_mail', False) and 'points' in vals:
            points_changes = {coupon: {'old': points_before[coupon], 'new': coupon.points} for coupon in self}
        db = firestore.client()
        if not self.env.context.get('loyalty_no_mail', False) and 'points' in vals:
            # Obtener el ID del res.partner asociado
            partner_id = self.partner_id.id
            # Obtener los puntos de fidelización actualizados
            points = self.points
            # Guardar los puntos en Cloud Firestore
            doc_ref = db.collection('loyalty_points')
            doc_ref.add({
                "id":partner_id,
                "points":points
            })
        return res