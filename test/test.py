# -*- coding:utf-8 -*-
import requests

import re

a = "class001"
b = a[-3:]
print re.match("\d\d\d", a[-3:])


# class A:
#     def __init__(self):
#         self.namea = "aaa"
#
#     def funca(self):
#         print "function a : %s" % self.namea
#
#
# class B(A):
#     def __init__(self):
#         # 这一行解决了问题
#         A.__init__(self)
#         self.nameb = "bbb"
#
#     def funcb(self):
#         print "function b : %s" % self.nameb
#
#
# b = B()
# print b.nameb
# b.funcb()
#
# b.funca()
#
#
# class A:
#     def __init__(self):
#         print("Enter A")
#         print("Leave A")
#
#
# class B(A):
#     def __init__(self):
#         print("Enter B")
#         A.__init__(self)
#         print("Leave B")
#
#
# class C(A):
#     def __init__(self):
#         print("Enter C")
#         A.__init__(self)
#         print("Leave C")
#
#
# class D(A):
#     def __init__(self):
#         print("Enter D")
#         A.__init__(self)
#         print("Leave D")
#
#
# class E(B, C, D):
#     def __init__(self):
#         print("Enter E")
#         B.__init__(self)
#         C.__init__(self)
#         D.__init__(self)
#         print("Leave E")
#
#
# E()


class A(object):
    def __init__(self):
        print("Enter A")
        print("Leave A")


class B(A):
    def __init__(self):
        print("Enter B")
        super(B, self).__init__()
        print("Leave B")


class C(A):
    def __init__(self):
        print("Enter C")
        super(C, self).__init__()
        print("Leave C")


class D(A):
    def __init__(self):
        print("Enter D")
        super(D, self).__init__()
        print("Leave D")


class E(B, C, D):
    def __init__(self):
        print("Enter E")
        super(E, self).__init__()
        print("Leave E")

        # E()
