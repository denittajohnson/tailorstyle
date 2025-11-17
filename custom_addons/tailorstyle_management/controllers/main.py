from odoo import http
from odoo.http import request

class TailorstyleWebsite(http.Controller):

    # Admin homepage
    @http.route('/admin_home', auth='user', website=True)
    def admin_home(self, **kw):
        return request.render('tailorstyle_management.homepage')

    # Redirect backend /web to admin_home
    @http.route('/web', type='http', auth='user')
    def redirect_to_admin_home(self, **kw):
        return request.redirect('/admin_home')

    # Redirect to existing backend views
    @http.route('/users', auth='user', website=True)
    def users_page(self, **kw):
        return request.redirect('/web#action=tailorstyle_management.action_tailorstyle_user')

    @http.route('/cloths', auth='user', website=True)
    def cloths_page(self, **kw):
        return request.redirect('/web#action=tailorstyle_management.action_tailorstyle_cloth')

    @http.route('/orders', auth='user', website=True)
    def orders_page(self, **kw):
        return request.redirect('/web#action=tailorstyle_management.action_tailorstyle_order')
