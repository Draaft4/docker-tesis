import firebase_admin
from firebase_admin import credentials, messaging
from odoo import models, fields, api
from odoo.http import request

class FirebaseNotificationIndividual(models.Model):
    _name = 'firebase.notification'
    title = fields.Char(string='Titulo', required=True)
    message = fields.Text(string='Mensaje', required=True)
    user_id = fields.Many2one('res.partner', string='User')

    # cred = credentials.Certificate('C:/Users/Pedro Neira/Documents/Tesis/odoo/dev/ups_firebase_service/static/services.json')  # Ruta archivo google-services.json
    # firebase_admin.initialize_app(cred)
    

    cred = credentials.Certificate('C:/Users/Pedro Neira/Documents/Tesis/odoo/dev/ups_firebase_service/static/services.json')
    firebase_admin.initialize_app(cred)

    def name_get(self):
        result = []
        for rec in self:
            result.append((rec.id, '%s%s' % ('Notificacion ',rec.id)))
        return result

    def send_notification(self):
        for record in self:
            registration_tokens = record.user_id.token_ids
            for tokens in registration_tokens:
                # print(tokens.token)
                message = messaging.Message(
                    notification=messaging.Notification(
                        title=record.title,
                        body=record.message,
                    ),
                    token=tokens.token,
                )
                response = messaging.send(message)
                print('Successfully sent message:', response)


class FirebaseNotificationGrupal(models.Model):

    _name="firebase.notification.grupal"
    title = fields.Char(string='Titulo', required=True)
    message = fields.Text(string='Mensaje', required=True)
    group_id = fields.Many2one("mass.notification")

    def name_get(self):
        result = []
        for rec in self:
            result.append((rec.id, '%s%s' % ('Notificacion ',rec.id)))
        return result

    def send_notification(self):
        for record in self:
            partner_records = self.env['res.partner'].sudo().search([('group_mass_notification', '=', record.group_id.id)])
            for partner in partner_records:
                registration_tokens = partner.token_ids
                for tokens in registration_tokens:
                    # print(tokens.token)
                    message = messaging.Message(
                        notification=messaging.Notification(
                            title=record.title,
                            body=record.message,
                        ),
                        token=tokens.token,
                    )
                    response = messaging.send(message)
                    print('Successfully sent message:', response)


class tokenListPartner(models.Model):

    _name = "token.partner"

    partner_id = fields.Many2one("res.partner")

    token = fields.Char()

    device_name = fields.Char(string="Nombre del dispositivo")

    def name_get(self):
        result = []
        for rec in self:
            result.append((rec.id, '%s%s' % ('Token ',rec.id)))
        return result


class massNotificationType(models.Model):

    _name="mass.notification"

    group_name = fields.Char(string="Grupo Notificaciones")

    def name_get(self):
        result = []
        for rec in self:
            result.append((rec.id, '%s' % (rec.group_name)))
        return result

class partnerInherit(models.Model):

    _inherit = "res.partner"

    token_ids = fields.One2many("token.partner","partner_id")

    group_mass_notification = fields.Many2one("mass.notification")



