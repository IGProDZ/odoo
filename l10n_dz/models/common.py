from openerp.osv import fields, osv

class AdditionalDiscountable(object):

    def record_currency(self, record):
        return record.pricelist_id.currency_id


    def _amount_all_generic(self, cls, cr, uid, ids, field_name, arg,context=None):
        cur_obj = self.pool.get('res.currency')
        res = super(cls, self)._amount_all(cr, uid, ids, field_name, arg, context)
        for record in self.browse(cr, uid, ids, context=context):
            o_res = res[record.id]
            cur = self.record_currency(record)

            def cur_round(value):
                """Round value according to currency."""
                return cur_obj.round(cr, uid, cur, value)

            old_amount_total =o_res['amount_total']

            # calcul Timbre
            o_res['amount_timbre'] = timbre = 0.0
            o_res['total_timbre'] = 0.0
            #    if record.payment_term and record.payment_term.payment_type  == 'cash':
            timbre = self.pool.get('config.timbre')._timbre(cr, uid, old_amount_total)
            o_res['amount_timbre'] = cur_round(timbre)
            o_res['total_timbre'] = old_amount_total + o_res['amount_timbre']
        return res

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
