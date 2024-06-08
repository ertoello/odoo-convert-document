# -*- coding: utf-8 -*-
# from odoo import http


# class OdooConvertDocument(http.Controller):
#     @http.route('/odoo_convert_document/odoo_convert_document', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/odoo_convert_document/odoo_convert_document/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('odoo_convert_document.listing', {
#             'root': '/odoo_convert_document/odoo_convert_document',
#             'objects': http.request.env['odoo_convert_document.odoo_convert_document'].search([]),
#         })

#     @http.route('/odoo_convert_document/odoo_convert_document/objects/<model("odoo_convert_document.odoo_convert_document"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('odoo_convert_document.object', {
#             'object': obj
#         })
