import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../tools'))

import files
import encdec
import number

from gmpy2 import mpz, mul, div


'''
    N_1:
    p = 13407807929942597099574024998205846127479365820592393377723561443721764030073662768891111614362326998675040546094339320838419523375986027530441562135724301 
    q = 13407807929942597099574024998205846127479365820592393377723561443721764030073778560980348930557750569660049234002192590823085163940025485114449475265364281

    N_2:
    p = 25464796146996183438008816563973942229341454268524157846328581927885777969985222835143851073249573454107384461557193173304497244814071505790566593206419759
    q = 25464796146996183438008816563973942229341454268524157846328581927885777970106398054491246526970814167632563509541784734741871379856682354747718346471375403

    N_3:
    p = 21909849592475533092273988531583955898982176093344929030099423584127212078126150044721102570957812665127475051465088833555993294644190955293613411658629209
    q = 32864774388713299638410982797375933848473264140017393545149135376190818117189240035825816494954711821626076210364113848440012285863311027426121370050758081

    C = 22096451867410381776306561134883418017410069787892831071731839143676135600120538004282329650473509424343946219751512256465839967942889460764542040581564748988013734864120452325229320176487916666402997509188729971690526083222067771600019329260870009579993724077458967773697817571267229951148662959627934791540

'''


def main(argv):
    lines      = files.read_lines(argv[0])
    N_1        = mpz(lines[0])
    N_2        = mpz(lines[1])
    N_3        = mpz(lines[2])
    C          = mpz(lines[3])
    E          = int(lines[4])

    p1, q1, i1 = number.factorize(N_1, 1)
    p2, q2, i2 = number.factorize(N_2, 1048576)
    p3, q3, i3 = number.factorize(mul(N_3, 24), 1)

    print
    print 'Factorization Demo'
    print
    print '       1st:'
    print 'Iterations: ', i1
    print '         p: ', p1
    print '         q: ', q1
    print ' Plaintext: ', encdec.rsa_decrypt(C, E, p1, q1, N_1)
    print
    print '       2nd:'
    print 'Iterations: ', i2
    print '         p: ', p2
    print '         q: ', q2
    print
    print '       3rd:'
    print 'Iterations: ', i3
    print '         p: ', div(p3, 6)
    print '         q: ', div(q3, 4)
    print


if __name__ == "__main__":
    main(sys.argv[1:])
