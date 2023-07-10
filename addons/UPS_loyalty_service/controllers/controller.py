from odoo import http
from odoo.http import request
from datetime import datetime
import json


class getClientData(http.Controller):

    @http.route('/api/loyaltyData', auth='public', website=False, crf=False, type='http', methods=['GET'])
    def getLoyalty(self, **kw):
        loyaltyList = []
        id_user = int(http.request.params.get('id'))
        loyaltyUsers = http.request.env['loyalty.card'].sudo().search([])
        program_id = 6
        for loyaltyUser in loyaltyUsers.filtered(lambda r: r.program_id.id == program_id):
            partner_id = loyaltyUser.partner_id.id
            if id_user == partner_id:
                loyaltyList.append({
                    'id': partner_id,
                    'points': loyaltyUser.points,
                })
                return request.make_response(json.dumps(loyaltyList), headers=[('Content-Type', 'application/json')])
        return http.request.make_response(json.dumps({'message': 'User not found'}),
                                          headers=[('Content-Type', 'application/json')])

    @http.route('/api/clientData', auth='public', website=False, crf=False, type='http', methods=['GET'])
    def getUserData(self, **kw):
        user_id = int(http.request.params.get('id'))
        user = http.request.env['res.partner'].sudo().browse(user_id)
        if user.exists():
            user_data = {
                'id': user.id,
                'name': user.name,
                'email': user.email,
                'phone': user.phone,
                'birth_date': user.x_birth_date.strftime('%Y-%m-%d'),
                'vat': user.vat
            }
            return http.request.make_response(json.dumps(user_data), headers=[('Content-Type', 'application/json')])
        else:
            return http.request.make_response(json.dumps({'message': 'User not found'}),
                                              headers=[('Content-Type', 'application/json')])

    @http.route('/api/login', type='http', auth='public', methods=['GET'], csrf=False)
    def sendLogin(self, **kwargs):
        email = http.request.params.get('email')
        contact = http.request.env['res.partner'].sudo().search(
            [('email', '=', email)])
        if contact:
            return json.dumps({'partner_id': contact.id, 'message': 'ok'
                               })
        else:
            return json.dumps({'partner_id': 0, 'message': 'error'})

    @http.route('/api/listcupons', type='http', auth='public', methods=['GET'], csrf=False)
    def getCupons(self, **kwargs):
        rewards = []
        loyalty_rewards = http.request.env['loyalty.reward'].sudo().search([])
        program_id = 6
        
        for reward in loyalty_rewards.filtered(lambda r: r.program_id.id == program_id):
            img =  reward.reward_product_id.image_128
            rewards.append({
                'description': reward.description,
                'required_points': reward.required_points,
                'reward_type': reward.reward_type,
                'quantity':reward.reward_product_qty,
                'base64':img.decode('utf-8')
            })
        return http.request.make_response(json.dumps(rewards), headers=[('Content-Type', 'application/json')])

    @http.route('/api/coupons', type='http', auth='public', methods=['GET'], csrf=False)
    def getCoupons(self, **kw):
        id_user = int(http.request.params.get('id'))
        coupons = http.request.env['loyalty.card'].sudo().search(
            [('partner_id', '=', id_user)])
        coupon_data = []
        for coupon in coupons:
            expiration_date = coupon.expiration_date
            if expiration_date:
                expiration_date = expiration_date.strftime('%Y-%m-%d')
                coupon_data.append({
                    'code': coupon.code,
                    'program_name': coupon.program_id.name,
                    'fecha de expiracion': expiration_date
                })

        return http.request.make_response(json.dumps(coupon_data), headers=[('Content-Type', 'application/json')])

    @http.route('/api/newClient', type='http', auth='public', methods=['POST'], csrf=False)
    def newClient(self, **post_data):
        try:
            data = json.loads(http.request.httprequest.data)
            name = data.get('name')
            email = data.get('email')
            vat = data.get('vat')
            x_birth_date_str = data.get('x_birth_date')
            x_birth_date = datetime.strptime(
                x_birth_date_str, '%Y-%m-%d').date()
            phone = data.get('phone')
            partner = http.request.env['res.partner'].sudo().create(
                {
                    'name': name,
                    'email': email,
                    'vat': vat,
                    'phone': phone,
                    'x_birth_date': x_birth_date
                })
            response = {
                'success': True,
                'partner_id': partner.id
            }
            return http.request.make_response(json.dumps(response), headers=[('Content-Type', 'application/json')])
        except Exception as e:
            error = {
                'fallo': False,
                'error': str(e)
            }
            return http.request.make_response(json.dumps(error), headers=[('Content-Type', 'application/json')])

    @http.route('/api/updateClient', type='http', auth='public', methods=['POST'], csrf=False)
    def updateClient(self, **post_data):
        try:
            client = json.loads(http.request.httprequest.data)
            partner_id = client.get('id')
            name = client.get('name')
            email = client.get('email')
            vat = client.get('vat')
            phone = client.get('phone')
            x_birth_date_str = client.get('x_birth_date')
            x_birth_date = datetime.strptime(
                x_birth_date_str, '%Y-%m-%d').date()
            partner = http.request.env['res.partner'].sudo().browse(
                int(partner_id))
            partner.write({
                'name': name,
                'email': email,
                'vat': vat,
                'phone': phone,
                'x_birth_date': x_birth_date
            })
            result = {
                'success': True,
                'message': 'Cliente actualizado correctamente'
            }
            return http.request.make_response(json.dumps(result), headers=[('Content-Type', 'application/json')])
        except Exception as e:
            error = {
                'success': False,
                'error': str(e)
            }
            return http.request.make_response(json.dumps(error), headers=[('Content-Type', 'application/json')])

    @http.route('/api/registerToken', type='http', auth='public', methods=['POST'], csrf=False)
    def registerToken(self, **post_data):
        try:
            data = json.loads(http.request.httprequest.data)
            partner_id = data.get('partner_id')
            token = data.get('token')
            device_name = data.get('device_name')
            partner = request.env['res.partner'].sudo().browse(int(partner_id))
            if not partner:
                raise ValueError('Partner not found')
            token_record = request.env['token.partner'].sudo().search(
                [('partner_id', '=', partner.id)], limit=1)
            request.env['token.partner'].sudo().create(
                {'partner_id': partner.id, 'token': token, 'device_name': device_name})
            result = {
                'success': True,
                'message': 'Token registered successfully'
            }
            return request.make_response(json.dumps(result), headers=[('Content-Type', 'application/json')])
        except Exception as e:
            error = {
                'success': False,
                'error': str(e)
            }
            return request.make_response(json.dumps(error), headers=[('Content-Type', 'application/json')])

    @http.route('/api/getContactTokens', type='http', auth='public', methods=['POST'], csrf=False)
    def getContactTokens(self, **post_data):
        try:
            data = json.loads(http.request.httprequest.data)
            partner_id = data.get('partner_id')
            # Validar existencia del partner
            print("Validar existencia del partner")
            partner = request.env['res.partner'].sudo().browse(int(partner_id))
            if not partner:
                raise ValueError('Partner not found')
            # Obtener tokens del contacto"
            print("Obtener tokens del contacto")
            token_records = request.env['token.partner'].sudo().search(
                [('partner_id', '=', partner.id)])
            tokens = []
            for token_record in token_records:
                tokens.append(
                    {'id': token_record.id, 'device_name': token_record.device_name, 'token': token_record.token})
            return request.make_response(json.dumps(tokens), headers=[('Content-Type', 'application/json')])
        except Exception as e:
            error = {
                'success': False,
                'error': str(e)
            }
            return request.make_response(json.dumps(error), headers=[('Content-Type', 'application/json')])

    @http.route('/api/deleteToken', type='http', auth='public', methods=['POST'], csrf=False)
    def deleteToken(self, **post_data):
        try:
            data = json.loads(http.request.httprequest.data)
            token_id = data.get('token_id')
            # Validar existencia del registro de token
            token_record = request.env['token.partner'].sudo().browse(
                int(token_id))
            if not token_record:
                raise ValueError('Token record not found')
            # Eliminar el registro de token
            token_record.unlink()
            result = {
                'success': True,
                'message': 'Token deleted successfully'
            }
            return request.make_response(json.dumps(result), headers=[('Content-Type', 'application/json')])
        except Exception as e:
            error = {
                'success': False,
                'error': str(e)
            }
            return request.make_response(json.dumps(error), headers=[('Content-Type', 'application/json')])
