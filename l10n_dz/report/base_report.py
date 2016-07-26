# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright (c) 2008 JAILLET Simon - CrysaLEAD - www.crysalead.fr
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsability of assessing all potential
# consequences resulting from its eventual inadequacies and bugs
# End users who are looking for a ready-to-use solution with commercial
# garantees and support are strongly adviced to contract a Free Software
# Service Company
#
# This program is Free Software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
#
##############################################################################

import time
import logging

from openerp.report import report_sxw

class base_report(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context=None):
        super(base_report, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'time': time,
            '_load': self._load,
            '_get_variable': self._get_variable,
            '_set_variable': self._set_variable,
        })
        self.context = context

    def _load(self, name, form):        
        fiscalyear = self.pool.get('account.fiscalyear').browse(self.cr, self.uid, form['fiscalyear_id'])
        period_ids=self.pool.get('account.period').search(self.cr, self.uid, [('fiscalyear_id', '=', form['fiscalyear_id'])])
        if period_ids:
            self.cr.execute("SELECT MIN(date_start) AS date_start, MAX(date_stop) AS date_stop FROM account_period WHERE id = ANY(%s)", (period_ids,))
            dates = self.cr.dictfetchall()
        else:
            dates = False
        if dates:
            self._set_variable('date_start', dates[0]['date_start'])
            self._set_variable('date_stop', dates[0]['date_stop'])            

        self.cr.execute("SELECT l10n_fr_line.code,definition FROM l10n_fr_line LEFT JOIN l10n_fr_report ON l10n_fr_report.id=report_id WHERE l10n_fr_report.code=%s",(name,))
        datas = self.cr.dictfetchall() 
        for line in datas: 
            if line['definition'].find('load_prev_year') == -1: 
                self._load_accounts(form,line['code'],eval(line['definition']),fiscalyear,period_ids,"current")
         
        self.cr.execute("SELECT * FROM account_fiscalyear WHERE id = %s", (form['fiscalyear_id'],))
        res = self.cr.dictfetchall()
        self.cr.execute("SELECT * FROM account_fiscalyear WHERE code = %s", (str(int(res[0]['code'])-1),))         
        res = self.cr.dictfetchall()
        if res:  
            fiscalyear = self.pool.get('account.fiscalyear').browse(self.cr, self.uid, res[0]['id'])
            period_ids=self.pool.get('account.period').search(self.cr, self.uid, [('fiscalyear_id', '=', res[0]['id'])])
            if period_ids:
                self.cr.execute("SELECT MIN(date_start) AS date_start, MAX(date_stop) AS date_stop FROM account_period WHERE id = ANY(%s)", (period_ids,))
                dates = self.cr.dictfetchall()
            else:
                dates = False
            if dates:
                self._set_variable('date_start', dates[0]['date_start'])
                self._set_variable('date_stop', dates[0]['date_stop'])            

            self.cr.execute("SELECT l10n_fr_line.code,definition FROM l10n_fr_line LEFT JOIN l10n_fr_report ON l10n_fr_report.id=report_id WHERE l10n_fr_report.code=%s",(name,))
            datas = self.cr.dictfetchall()
            for line in datas:
                if line['definition'].find('load_prev_year') != -1: 
                    self._load_accounts(form,line['code'],eval(line['definition']),fiscalyear,period_ids,"previous")
             
    def _set_variable(self, variable, valeur):
        self.localcontext.update({variable: valeur})

    def _get_variable(self, variable):
        return self.localcontext[variable]

    def _load_accounts(self, form, code, definition, fiscalyear, period_ids, year):
        logging.warning("Amine23081304 je suis au debut")   	
        accounts = {}
        if year == "current":            
            for x in definition['load']:
                p = x.split(":")
                accounts[p[1]] = [p[0],p[2]]
        elif year == "previous":
            for x in definition['load_prev_year']:
                p = x.split(":")
                accounts[p[1]] = [p[0],p[2]]				
        sum = 0.0
        if fiscalyear.state != 'done' or not code.startswith('bpcheck'):
            query_params = []
            query_cond = "("
            for account in accounts:
                logging.warning("Amine23081304 accounts %s",account)				
                query_cond += "aa.code LIKE '" + account + "%%' OR "
            query_cond = query_cond[:-4]+")"

            if len(definition['except']) > 0:
                query_cond = query_cond+" and ("
                for account in definition['except']:
                    query_cond += "aa.code NOT LIKE '"+account+"%%' AND "
                query_cond = query_cond[:-5]+")"

            closed_cond = ""
            if fiscalyear.state == 'done':
                closed_cond=" AND (aml.move_id NOT IN (SELECT account_move.id as move_id FROM account_move WHERE period_id = ANY(%s) AND journal_id=(SELECT res_id FROM ir_model_data WHERE name='closing_journal' AND module='l10n_fr')) OR (aa.type != 'income' AND aa.type !='expense'))"
                query_params.append(list(period_ids))
#            context = {}				
#            data = {}
#            data['ids'] = context.get('active_ids', [])
#            data['model'] = context.get('active_model', 'ir.ui.menu')
#            data['form'] = self.read(cr, uid, ids, ['target_move'], context=context)[0] 				
#            logging.warning("Amine09111909 %s",data['form'])  				
            logging.warning("Amine23081304 accounts %s",accounts[p[1]][1])               			
            if (accounts[p[1]][1] == 'MVM5') or (accounts[p[1]][1] == 'MVMD5') or (accounts[p[1]][1] == 'MVMC5'): 				
                query = "SELECT aa.code AS code, SUM(debit) as debit, SUM(credit) as credit " \
                    " FROM account_move_line aml LEFT JOIN account_account aa ON aa.id=aml.account_id "\
                    " WHERE "+query_cond+closed_cond+" AND aml.state='valid' AND aml.period_id = ANY(%s) AND aml.move_id IN (select DISTINCT aml.move_id FROM account_move_line aml LEFT JOIN account_account aa ON aa.id=aml.account_id WHERE aa.code LIKE '51%%' OR aa.code LIKE '52%%' OR aa.code LIKE '53%%' OR aa.code LIKE '54%%' OR aa.code LIKE '58%%') GROUP BY code"
            else:
                query = "SELECT aa.code AS code, SUM(debit) as debit, SUM(credit) as credit " \
                    " FROM account_move_line aml LEFT JOIN account_account aa ON aa.id=aml.account_id "\
                    " WHERE "+query_cond+closed_cond+" AND aml.state='valid' AND aml.period_id = ANY(%s) GROUP BY code"
            query_params.append(list(period_ids))
            self.cr.execute(query, query_params)
            lines =self.cr.dictfetchall()
            for line in lines:
                logging.warning("Amine23081304 code %s",line["code"])				
                for account in accounts:
                    logging.warning("Amine23081304 accounts2 %s",account)    					
                    if(line["code"].startswith(account)):                              					
                        logging.warning("Amine23081304 code2 %s",line["code"])
                        operator=accounts[account][0]
                        type=accounts[account][1]
                        value=0.0
                        if(type == "S"):
                            value=line["debit"]-line["credit"]  
                            logging.warning("Amine23081304 value %s",value) 								
                        elif(type == "D") or (type == "MVM5"):
                            value=line["debit"]-line["credit"]                            
                            if(abs(value)<0.001): value=0.0
                        elif(type == "C"):
                            value=line["credit"]-line["debit"]                            
                            if(abs(value)<0.001): value=0.0
                        elif(type == "MVMD5") or (type == "Dr"):                            
                            value=line["debit"]
                            if(abs(value)<0.001): value=0.0							
                        elif(type == "MVMC5"):                            
                            value=line["credit"]
                            if(abs(value)<0.001): value=0.0
                        elif(type == "SD"):                            
                            value=line["debit"]-line["credit"]
                            if(value < 0) or (abs(value)<0.001): value=0.0                                
                        elif(type == "SC"):                            
                            value=line["credit"]-line["debit"]
                            if(value < 0) or (abs(value)<0.001): value=0.0							
                        if(operator == '+'):
                            sum += value                                									
                        else:
                            sum -= value
                        logging.warning("Amine23081304 sum %s",sum)  								
                        break
        logging.warning("Amine23081304 codesum2 %s",code) 							
        logging.warning("Amine23081304 sum2 %s",sum)             			
        self._set_variable(code, sum)
          
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
