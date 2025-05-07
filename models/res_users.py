# -*- coding: utf-8 -*-
from openerp import models, fields, api
import uuid


class ResUsers(models.Model):
    _inherit = 'res.users'

    api_key = fields.Char(string='Clé API', readonly=True)

    @api.multi
    def generate_api_key(self):
        for user in self:
            user.api_key = str(uuid.uuid4())
