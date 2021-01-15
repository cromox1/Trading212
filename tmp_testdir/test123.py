## 'index ) element'
test1 = ('abc', 'bcd')
for ele in test1:
    print(test1.index(ele)+1, ')', ele)

## multi slicing
test2 = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l']
print(" // ".join(test2))
print(" // ".join(test2[0:3] + test2[-2:]))
print(test2[0:3] + test2[int(2*len(test2)/3):])

## test guna yield

listing = (4, 22, 24, 34, 46, 56)
def multislice(a,sl):
    for si in sl:
        yield a[si]
        # return a[si]

print(list(multislice(listing,[slice(0,3),slice(4,5)])))
print(list(multislice(listing,[slice(0,3),slice(4,5),slice(3,None)])))

## reverse LIST

test3 = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l']
print(test3)            	# original list
print(test3[::-1])    	    # reverse list

range1 = [x * 7.85 for x in range(1, 1 + int(427/7.85))]
print(range1)