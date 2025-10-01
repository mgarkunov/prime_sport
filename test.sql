with clnd as (select datum::date AS calendar_date, sku_1c
              from generate_series(
                           (select min(report_date) from sales),
                           (select max(report_date) from sales),
                           '1 day'::interval
                   ) AS gs(datum)
                       cross join (select distinct sku_1c from catalog) as c),
     tb as (select s.report_date::date as report_date,
                   c.sku_1c            as sku_1c,
                   c.name              as name,
                   sum(
                           (s.item_price * s.quantity) - cp.cost -
                           ((s.item_price * s.quantity) * s.commission_pnt) -
                           s.logistic_price
                   )
                                       as gross_profit
            from catalog as c
                     left join sales as s
                               on c.sku_1c = s.sku_1c
                     left join cost_price as cp
                               on c.sku_1c = cp.sku_1c
            group by 1, 2, 3
            order by 1, 2)
select clnd.calendar_date as report_date,
       clnd.sku_1c        as sku_1c,
       tb.gross_profit    as gross_profit,
       avg(tb.gross_profit) over (
           partition by clnd.sku_1c
           order by clnd.calendar_date
           rows between 15 preceding and 1 preceding
           )
                          as gross_profit_avg15
from clnd
left join tb
on clnd.calendar_date = tb.report_date
   and clnd.sku_1c = tb.sku_1c