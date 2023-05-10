from odoo import api, fields, models, tools
from datetime import datetime

class tanHrLeaveType(models.Model):
    _inherit = 'hr.leave.type'
    effectoffdays =fields.Boolean(string='Deduct weekend days',default=False)


    @api.model
    def create(self, vals_list):
        res = super(tanHrLeaveType, self).create(vals_list)
        return res


class tanmya_Hrleave(models.Model):
    _inherit = 'hr.leave'


    def _compute_number_of_days(self):
        super(tanmya_Hrleave,self)._compute_number_of_days()
        for holiday in self:
            if holiday.holiday_status_id.effectoffdays:
                 unusaldays=holiday.employee_id._get_unusual_days(holiday.date_from,holiday.date_to)
                 print(unusaldays)
                 if unusaldays:
                     holiday.number_of_days =holiday.number_of_days+len([elem for elem in unusaldays.values() if elem ])

class tanmya_EmpLeave(models.Model):
    _inherit = 'hr.employee'

    lost_leaves_current=fields.Integer(string='Current Lost leaves',compute='_calc_lost_leaves')
    lost_leaves_previous = fields.Integer(string='Previous Lost leaves',compute='_calc_pre_lost_leaves')
    sum_leaves =fields.Integer(string="total available",compute='_calc_total_leaves')
    # sum_taken =fields.Integer(string="total taken",compute='_calc_total_taken')

    def _calc_pre_lost_leaves(self):
        currentyear = datetime(datetime.today().year-1, 1, 1)
        nextyear = datetime(datetime.today().year , 1, 1)
        query = f"""
                select sum(q.lost) as result from (
        select hr_leave_allocation.number_of_days- COALESCE(sum(leaves.totleave),0) as lost
        from hr_leave_allocation left join
        (select sum(number_of_days) as totleave,hr_leave.holiday_allocation_id from hr_leave
        where date_from >='{currentyear}' and date_to<'{nextyear}' and employee_id={self.id} and state='validate'
        group by holiday_allocation_id) as leaves
          on hr_leave_allocation.id= leaves.holiday_allocation_id
        where 
        hr_leave_allocation.date_from >='{currentyear}' and hr_leave_allocation.date_to<'{nextyear}'
        and hr_leave_allocation.employee_id={self.id} and hr_leave_allocation.state='validate'
        group by hr_leave_allocation.number_of_days) as q
                 """
        new_cr = self._cr
        new_cr.execute(query)
        values = new_cr.dictfetchone()
        if values:
            self.lost_leaves_previous = values.get('result')
        else:
            self.lost_leaves_previous = 0

    def _calc_lost_leaves(self):
        currentyear =datetime(datetime.today().year , 1, 1)
        nextyear = datetime(datetime.today().year+1, 1, 1)
        query=f"""
        select sum(q.lost) as result from (
select hr_leave_allocation.number_of_days- COALESCE(sum(leaves.totleave),0) as lost
from hr_leave_allocation left join
(select sum(number_of_days) as totleave,hr_leave.holiday_allocation_id from hr_leave
where date_from >='{currentyear}' and date_to<'{datetime.today()}' and employee_id={self.id} and state='validate'
group by holiday_allocation_id) as leaves
  on hr_leave_allocation.id= leaves.holiday_allocation_id
where 
hr_leave_allocation.date_from >='{currentyear}' and hr_leave_allocation.date_to<'{datetime.today()}'
and hr_leave_allocation.employee_id={self.id} and hr_leave_allocation.state='validate'
group by hr_leave_allocation.number_of_days) as q
         """
        new_cr = self._cr
        new_cr.execute(query)
        values = new_cr.dictfetchone()
        if values:
            self.lost_leaves_current = values.get('result')
        else:
            self.lost_leaves_current = 0

    def _calc_total_leaves(self):
        bofyear=datetime(datetime.today().year, 1, 1)
        records_sum = sum(self.env["hr.leave.allocation"].search([('employee_id','=',self.id),('state','=','validate'),('date_from','>=',bofyear)]).mapped('number_of_days'))
        qquery=f"""select  sum(hr_leave_allocation.number_of_days)-sum(hr_leave.number_of_days) as lostleaves from hr_leave right join hr_leave_allocation
               on  (hr_leave.holiday_allocation_id=hr_leave_allocation.id )
               where hr_leave_allocation.date_to<'{datetime.today()}' and hr_leave.employee_id={self.id}"""

        self.sum_leaves=records_sum

    def _calc_total_taken(self):
        self.sum_taken=0

class tanmya_leaveAllocate(models.Model):
    _inherit = "hr.leave.allocation"

    def _end_of_year_accrual(self):
        #todo
        super(tanmya_leaveAllocate,self)._end_of_year_accrual()


