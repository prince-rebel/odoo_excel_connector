# -*- coding: utf-8 -*-
from openerp import http
from openerp.http import request
from datetime import datetime, date


class CreancesClientsAPI(http.Controller):

    @http.route('/api/creances_clients', type='json', auth='user')
    def get_creances_clients(self, **kwargs):
        today = date.today()
        result = []

        invoices = request.env['account.invoice'].sudo().search([
            ('type', '=', 'out_invoice'),
            ('state', 'in', ['open', 'paid']),
        ])

        for inv in invoices:
            if inv.state == 'paid':
                reste_a_payer = 0.0
                reglement = inv.amount_total
                statut = "Payée"
                jours_retard = ""
            else:
                reste_a_payer = inv.residual
                reglement = inv.amount_total - inv.residual
                statut = "Non payée"
                if inv.date_due:
                    due_date = datetime.strptime(inv.date_due, "%Y-%m-%d").date()
                    jours_retard = (today - due_date).days if today > due_date else ""
                else:
                    jours_retard = ""

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

        return result
