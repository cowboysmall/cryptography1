import sys
import time

from numbthy import powmod, invmod



P = 13407807929942597099574024998205846127479365820592393377723561443721764030073546976801874298166903427690031858186486050853753882811946569946433649006084171
G = 11717829880366207009516117596335367088558084999998952205599979459063929499736583746670572176471460312928594829675428279466566527115212748467589894601965568
H = 3239475104050450443565264378728065788649097520952449527834792452971981976143292558073856937958553180532878928001494706097394108577585732452307673444020333



'''
x should be equal to 375374217830
                     375374217830
                     375374217830
'''
def main():
    print
    print "Discrete Log Demo (numbthy)"
    print

    g_to_b     = powmod(G, 1048576, P)
    g_invert   = invmod(G, P)
    map        = {}


    time_start = time.time()
    calc_1     = powmod(H * G, 1, P)
    for i in range(1048576 + 1):
        calc_1 = powmod(calc_1 * g_invert, 1, P)
        map[calc_1] = i
    time_end   = time.time()


    print
    print 'Left side complete'
    print 'in time: %0.3f ms' % ((time_end - time_start) * 1000.0)
    print


    time_start = time.time()
    calc_0     = invmod(g_to_b, P)
    calc       = None
    for j in range(1048576 + 1):
        calc_0 = powmod(calc_0 * g_to_b, 1, P)
        if calc_0 in map:
            calc = (j * 1048576) + map[calc_0]
            break
    time_end = time.time()


    print 
    print 'Successfully found x with a value of %s' % calc
    print 'in time: %0.3f ms' % ((time_end - time_start) * 1000.0)
    print



if __name__ == "__main__":
    main()