#!/usr/bin/env python2
from matplotlib import pyplot as plt
import numpy as np
from scipy.interpolate import InterpolatedUnivariateSpline as ius
from scipy.optimize import bisect as bs
from copy import copy
data = '''
-1000.1       -5.30647541404105E-02   0.860013439593021
-949.975      -5.28408094143352E-02   0.856383997088847
-899.85       -5.20729892914885E-02   0.843940038089416
-849.925      -5.21387717337086E-02   0.8450061654147
-799.975      -5.13320485674585E-02   0.831931709945249
-749.975      -4.90683050673635E-02   0.795243518971602
-700.2        -4.83901370846416E-02   0.784252540328806
-649.9        -4.70388219214658E-02   0.762351954520342
-600.15       -4.78853765042068E-02   0.776071952479438
-549.875      -4.69794216899358E-02   0.761389262838109
-499.9        -4.70737143237943E-02   0.762917451061848
-449.95       -4.73181631033159E-02   0.766879200043561
-399.8        -4.68963307884461E-02   0.76004261960671
-349.95       -4.72937378512328E-02   0.76648334321925
-300.05       -4.77740489945072E-02   0.774267682279962
-249.85       -0.047303656670089      0.766644096202267
-200.1        -4.78849899698874E-02   0.776065687968936
-150.1        -4.76237124880034E-02   0.771831198437736
-99.025       -0.047226874734163      0.765399701539859
-49.3         -4.83753064776643E-02   0.784012182646491
0.45          -4.78536444473938E-02   0.775557675238976
49.975        -4.85616114636211E-02   0.787031602869602
99.9          -4.99137347265351E-02   0.808945285443453
149.9         -5.92413989431258E-02   0.960117503542358
199.75        -7.09707301767545E-02   1.15021322077997
249.6         -7.85876799322312E-02   1.27366011626697
299.6         -8.53675079836319E-02   1.3835398912096
349.1         -0.08872878389617       1.43801564457528
400.2         -0.089549536583423      1.45131747463279
448.95        -8.98141859486887E-02   1.45560661183121
499.275       -9.00835800723359E-02   1.45997264670006
549.375       -8.93425815278834E-02   1.44796338146796
599.375       -8.99772875057709E-02   1.45824997715686
650.125       -8.92753197398012E-02   1.4468732785803
700.05        -0.090069159228884      1.45973893000091
749.875       -8.93302478572607E-02   1.44776349130232
799.725       -8.99741016201931E-02   1.45819834393141
849.7         -8.96219838426534E-02   1.45249161776431
899.8         -8.92663929451906E-02   1.44672860320279
949.8         -8.88177690063115E-02   1.43945781446535
999.675       -8.88436472274759E-02   1.43987721936705
999.9         -8.96662125241229E-02   1.45320842614486
949.6         -8.93724175012527E-02   1.44844692913527
899.95        -8.99813531447674E-02   1.45831586842941
849.95        -9.06072161709186E-02   1.46845914757115
799.825       -9.02651543161011E-02   1.46291539641126
750.15        -9.03285948800217E-02   1.46394356922523
699.975       -9.05103177943285E-02   1.46688872842021
650.025       -0.090495874330095      1.46665464510905
600.025       -9.01107242652538E-02   1.46041256903823
550.1         -9.02595235967469E-02   1.46282414008873
499.975       -9.03935060662126E-02   1.46499557621949
449.925       -9.07604577149682E-02   1.47094271297198
399.975       -0.090685022779988      1.46972014897543
349.9         -9.05810635150682E-02   1.46803529494286
299.925       -9.00897818672599E-02   1.46007315836869
250.075       -9.03666890496494E-02   1.46456095638514
199.9         -9.04908004948738E-02   1.46657241413387
150.2         -8.99821450516299E-02   1.458328702759
99.025        -9.06556952863642E-02   1.46924484217199
49.45         -0.091057520320864      1.47575716726673
0             -0.090412858940442      1.46530922568798
-50.2         -9.02387676210874E-02   1.46248775074126
-100.05       -8.86535907071909E-02   1.43679699852414
-149.8        -7.79402928992487E-02   1.26316800039831
-199.7        -6.69010751913643E-02   1.08425686163655
-249.4        -5.88837944740374E-02   0.954321855292282
-299.6        -0.052160243879768      0.845354161640955
-349.3        -4.87414771995882E-02   0.789946663021293
-399.575      -4.87597713611464E-02   0.790243154073801
-449.1        -4.79863261997287E-02   0.777708030819534
-499.125      -4.81653364357465E-02   0.780609225996895
-549.1        -0.047269698908431      0.766093747258277
-599.6        -4.80904870604529E-02   0.779396152088604
-649.75       -4.84079761523022E-02   0.784541655734812
-699.8        -4.72742237354863E-02   0.766167080530848
-749.7        -4.70759455450799E-02   0.7629536121696
-799.8        -4.73933330689166E-02   0.768097469716484
-849.825      -4.69718232312647E-02   0.761266115625176
-899.9        -4.70108328063436E-02   0.761898338639946
-949.75       -0.046559952167593      0.754590975866687
-999.8        -4.69771093055334E-02   0.761351786330476'''

data = [i for i in data.split("\n") if i]
data = [i.split() for i in data]
B = [float(i[0]) for i in data]
y = [float(i[2]) for i in data]
Bp = B[:41]
yp = y[:41]
Bn = list(reversed(B[41:]))
yn = list(reversed(y[41:]))
p = ius(Bp, yp)
n = ius(Bn, yn)
newx = np.linspace(-1000,1000,500)
plt.plot(B, y, label = 'Linear interpolated')
plt.scatter(B, y, 80, marker = 'x', color='black', label='Experiment data')
plt.xlabel("Magnetic Field B/mT")
plt.ylabel("Kerr Angle $\\theta$/degree")
plt.legend(loc = 'upper left')
plt.show()
plt.plot(newx, p(newx), color = 'red', label = "Increasing side curve")
plt.plot(newx, n(newx), color = 'blue', label = "Decreasing side curve")
plt.xlabel("Magnetic Field B/mT")
plt.ylabel("Kerr Angle $\\theta$/degree")
plt.scatter(B, y, 80, marker = 'x', color='black', label='Experiment data')
plt.legend(loc = 'upper left')
plt.show()
ysorted = copy(y)
ysorted.sort()
ymin = sum(ysorted[:5]) / 5
ymax = sum(ysorted[-5:]) / 5
print "theta = ", (ymax - ymin) / 2
ymed = (ymin + ymax) / 2
u0 = 1.25663e-6
incB = bs(lambda x: p(x) - ymed, -1000, 1000)
decB = bs(lambda x: n(x) - ymed, -1000, 1000)
incH = incB * 1e-3 / u0
decH = decB * 1e-3 / u0
print incH, decH
