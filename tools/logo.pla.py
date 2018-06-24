import pla

a = pla.Asm()

a.op_0001(320, 200, 5)
a.op_0023('TR.ptr')
a.op_0029('TEXTS.key')
a.op_0028('ghost.til', 0)
a.op_0019('gene.chv')

a.op_0031(0, 255, 255, 255)
a.op_0031(1, 224, 120, 40)

a.op_0032(1)
a.op_0003('ANIx01.ANI', 0)
a.op_0004(0, 0, 32768, 0, 0)
a.op_0010(232, 3, 0)

a.op_002e(0, 320, 64)
a.op_002e(1, 320, 64)

a.op_0032(0)
a.op_002a(0, 28000)
a.op_002a(0, 28001)

a.op_0032(1)
a.op_002a(1, 28002)
a.op_002a(1, 28003)

a.op_002c(0, 0, 23, 70)

a.op_0007(30)

a.op_002d(1)

a.op_002c(0, 0, 0, 0)

a.op_002d(1)
a.op_0007(30)


a.op_000a()
a.op_0011(232, 5)


a.op_0032(0)
a.op_0006(0)
a.op_0010(232, 5, 0)
a.op_0019('INTRO.CHV')
a.op_002e(6, 320, 40)
a.op_002e(7, 320, 40)
a.op_002a(6, 28010)
a.op_002a(7, 28020)
a.op_002c(6, 0, 0, 50)
a.op_002c(7, 0, 0, 93)
a.op_0007(50)
a.op_002d(6)
a.op_002d(7)
a.op_0011(232, 5)
a.op_000a()

a.run()
