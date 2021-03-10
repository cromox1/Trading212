buysell_point = {'GBP/USD': -7, 'EUR/USD': -7, 'USD/JPY': 7, 'USD/CHF': 2, 'USD/CAD': 5, 'AUD/USD': -2, 'NZD/USD': -2}
open_position = {'USD/CAD': -0.19, 'NZD/USD': 0.47}

limit_buysell = 3
buymark = -6
sellmark = 6

to_buysell_instr = {}
for kk,vv in buysell_point.items():
    if vv > sellmark or vv < buymark:
        to_buysell_instr[kk] = vv

print('TO_BUYSELL_INTSR =', to_buysell_instr)
print('LEN(TO_BUYSELL_INTSR) =', len(to_buysell_instr))
for i in range(len(to_buysell_instr)):
    print('i=', i, ' // ', list(to_buysell_instr.keys())[i])

list_to_buysell = []
for kk, vv in buysell_point.items():
    if vv > sellmark or vv < buymark:
        list_to_buysell.append(kk)

print('LIST_TO_BUYSELL =', list_to_buysell)

list1 = [vv for vv in list(buysell_point.keys()) if buysell_point[vv] > sellmark or buysell_point[vv] < buymark]
print('LIST1 =', list1)

print('LIST NDAK =', list1[:1])

