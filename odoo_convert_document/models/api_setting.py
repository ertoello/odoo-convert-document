import convertapi
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ApiSettings(models.Model):
    _name = 'api.settings'
    _description = 'Api Settings'

    secret_key = fields.Char('API Secret Key')
    name = fields.Char('Account Name')
    email = fields.Char('Email')
    id_account = fields.Char('Account ID')
    convert_limit = fields.Integer('Remaining Conversion Limits')
    max_workers = fields.Integer('Maximum Workers Count')
    is_active = fields.Boolean('Active')
    state = fields.Selection([
        ('active', 'Active'),
        ('non_active', 'Non Active'),
    ], string='Status', default=('non_active'))
    percentage = fields.Float('Percentage', compute="_compute_progression")

    def name_get(self):
        res = []
        for rec in self:
            res.append((rec.id, '%s / %s' % (rec.name, rec.id_account)))
        return res

    def action_connect(self):
        for vals in self:
            try:
                convertapi.api_secret = vals.secret_key
                value = convertapi.user()
                vals.is_active = True
                vals.name = value['FullName']
                vals.email = value['Email']
                vals.state = 'active'
                vals.id_account = value['Id']
                vals.convert_limit = value['SecondsLeft']
                vals.max_workers = value['MaxWorkers']
            except:
                raise ValidationError("Error Connecting to API")

    @api.depends('convert_limit')
    def _compute_progression(self):
        for percen in self:
            percen.percentage = 0
            if percen.convert_limit:
                x = percen.convert_limit / 250 * 100
                percen.percentage = 100 - x

    def action_disconnect(self):
        for res in self:
            res.is_active = False
            res.state = 'non_active'
