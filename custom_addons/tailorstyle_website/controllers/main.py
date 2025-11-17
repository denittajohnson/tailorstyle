from odoo import http
from odoo.http import request
from odoo.exceptions import ValidationError

class TailorStyleWebsite(http.Controller):

    # -------------------- Home Page --------------------
    @http.route('/', type='http', auth='public', website=True)
    def home(self, **kw):
        return request.render('tailorstyle_website.home_page')

    # -------------------- Collections Page --------------------
    @http.route('/collections', type='http', auth='public', website=True)
    def collections(self, **kw):
        
        clothes = request.env['tailorstyle.cloth'].sudo().search([('show_in_website', '=', True)])
        return request.render('tailorstyle_website.collections_page', {'clothes': clothes})

    # -------------------- Registration --------------------
    @http.route('/register', type='http', auth='public', website=True)
    def registration_page(self, **kw):
        return request.render('tailorstyle_website.registration_page')

    @http.route('/register/submit', type='http', auth='public', methods=['POST'], website=True, csrf=False)
    def submit_registration(self, **post):
        name = post.get('name','').strip()
        phone = post.get('phone','').strip()
        place = post.get('place','').strip()
        password = post.get('password','').strip()

        existing_user = request.env['tailorstyle.user'].sudo().search([('phone', '=', phone)], limit=1)
        if existing_user:
            return request.render('tailorstyle_website.registration_page', {
                'already_registered': True,
                'user': existing_user,
                'name': name,
                'phone': phone,
                'place': place
            })

        user_vals = {
            'name': name,
            'phone': phone,
            'place': place,
            'password': password,
        }
        
        try:
            request.env['tailorstyle.user'].sudo().create(user_vals)
        except ValidationError as e:
            
            return request.render('tailorstyle_website.registration_page', {
                'error': str(e),
                'name': name,
                'phone': phone,
                'place': place
        })
            
        return request.render('tailorstyle_website.registration_page', {
            'registration_success': True,
            'name': name
        })


    # -------------------- Order Form --------------------
    @http.route('/order/<int:cloth_id>', type='http', auth='public', website=True)
    def order_page(self, cloth_id, **kw):
        cloth = request.env['tailorstyle.cloth'].sudo().browse(cloth_id)
        return request.render('tailorstyle_website.order_page', {'cloth': cloth})

    @http.route('/order/submit', type='http', auth='public', methods=['POST'], website=True, csrf=False)
    def submit_order(self, **post):
        cloth_id = int(post.get('cloth_id') or 0)
        name = post.get('name').strip()
        phone = post.get('phone').strip()
        is_urgent = 'urgent' in post
        date_needed = post.get('urgent_date') if is_urgent else False
        
        bubbled_choice = post.get('bubbled') or False
        
        if not name or not phone:
            return request.render('tailorstyle_website.order_page', {
                'cloth': request.env['tailorstyle.cloth'].sudo().browse(cloth_id),
                'error': "Name and phone are required."
            })
        
        # Check if user exists
        user = request.env['tailorstyle.user'].sudo().search([('name', '=ilike', name), ('phone', '=', phone)], limit=1)
        if not user:
            return request.render('tailorstyle_website.user_not_found')

        cloth = request.env['tailorstyle.cloth'].sudo().browse(cloth_id)
        if not cloth:
            return request.render('tailorstyle_website.user_not_found')
        
        if cloth.stock <= 0:
            return request.render('tailorstyle_website.order_page', {
                'cloth': cloth,
                'out_of_stock': True
            })

        # Server-side validate urgent_date is present and not in the past
        if is_urgent:
            if not date_needed:
                return request.render('tailorstyle_website.order_page', {
                    'cloth': cloth,
                    'error': "Please select a date for urgent orders."
                })
            # compare dates: urgent_date >= today (use date strings 'YYYY-MM-DD')
            from datetime import date, datetime
            try:
                picked = datetime.strptime(date_needed, '%Y-%m-%d').date()
            except Exception:
                return request.render('tailorstyle_website.order_page', {
                    'cloth': cloth,
                    'error': "Invalid date format."
                })
            if picked < date.today():
                return request.render('tailorstyle_website.order_page', {
                    'cloth': cloth,
                    'error': "Urgent date cannot be earlier than today."
                })
                
            # If cloth has allow_bubbled_option False, ignore bubbled_choice
        if not cloth.allow_bubbled_option:
            bubbled_choice = False
            
        order_vals = {
            'cloth_id': cloth.id,
            'user_id': user.id,
            'is_urgent': bool(is_urgent),
            'urgent_date': date_needed or False,
            'status': 'ordered'
        }
        
        if bubbled_choice:
            order_vals['bubbled'] = bubbled_choice
        
        order = request.env['tailorstyle.order'].sudo().create(order_vals)
        # Pass success flag and order object to same page
        return request.render('tailorstyle_website.order_page', {
            'cloth': cloth,
            'order_success': True,
            'order': order
        })


        # Reduce stock
        #new_stock = max(cloth.stock -1, 0)
        #cloth.sudo().write({'stock': new_stock})

        #return request.render('tailorstyle_website.order_success', {'order': order})

    # -------------------- Show My Orders --------------------
    @http.route('/my_orders', type='http', auth='public', website=True)
    def my_orders(self, phone=None, **kw):
        if not phone:
            # No phone provided, can't show orders
            return request.render('tailorstyle_website.user_not_found')

        # Find user by phone
        user = request.env['tailorstyle.user'].sudo().search([('phone', '=', phone)], limit=1)
        if not user:
            return request.render('tailorstyle_website.user_not_found')

        # Fetch orders for this user
        orders = request.env['tailorstyle.order'].sudo().search([('user_id', '=', user.id)])
        return request.render('tailorstyle_website.orders_page', {'orders': orders, 'user': user})

    @http.route('/my_orders/cancel/<int:order_id>', type='http', auth='public', methods=['POST'], website=True, csrf=False)
    def cancel_order(self, order_id, **post):
        order = request.env['tailorstyle.order'].sudo().browse(order_id)
        if order.status == 'ordered':
            order.sudo().write({'status': 'cancelled'})
        return request.redirect('/my_orders?phone=%s' % order.user_id.phone)

    

    
    
    