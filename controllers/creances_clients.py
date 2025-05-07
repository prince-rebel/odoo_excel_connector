# -*- coding: utf-8 -*-
from openerp import http
from openerp.http import request, Response
from datetime import datetime, date
import json


class CreancesClientsAPI(http.Controller):

    @http.route('/api/creances_clients', type='http', auth='none', methods=['GET'])
    def get_creances_clients(self, **kwargs):
        token = request.httprequest.headers.get('X-API-KEY')
        if not token:
            return Response(json.dumps({'error': 'Clé API manquante'}), status=401, content_type='application/json')

        user = request.env['res.users'].sudo().search([('api_key', '=', token)], limit=1)
        if not user:
            return Response(json.dumps({'error': 'Clé API invalide'}), status=403, content_type='application/json')

        today = date.today()
        result = []

        invoices = request.env['account.invoice'].sudo().search([
            ('type', '=', 'out_invoice'),
            ('state', 'in', ['open', 'paid']),
            ('user_id', '=', user.id)
        ])

        for inv in invoices:
            reste_a_payer = inv.residual if inv.state == 'open' else 0.0
            reglement = inv.amount_total - reste_a_payer
            statut = "payée" if inv.state == 'paid' else "non payée"

            jours_retard = 0
            if inv.state != 'paid' and inv.date_due:
                due_date = datetime.strptime(inv.date_due, "%Y-%m-%d").date()
                jours_retard = max((today - due_date).days, 0) if today > due_date else 0

            date_fact = inv.date_invoice and datetime.strptime(inv.date_invoice, "%Y-%m-%d").date() or ''
            due_date = inv.date_due and datetime.strptime(inv.date_due, "%Y-%m-%d").date() or ''
            nb_jours_echeance = (due_date - date_fact).days if due_date and date_fact else ''

            result.append({
                "commercial": inv.user_id.name if inv.user_id else '',
                "numero_facture": inv.number or '',
                "client": inv.partner_id.name or '',
                "tva": inv.amount_tax,
                "ht": inv.amount_untaxed,
                "date_facturation": str(date_fact),
                "nb_jours_echeance": nb_jours_echeance,
                "reglement": reglement,
                "reste_a_payer": reste_a_payer,
                "statut_reglement": statut,
                "jours_retard": jours_retard
            })

        return Response(json.dumps(result), content_type='application/json;charset=utf-8', status=200)
