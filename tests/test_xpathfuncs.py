from parsel import Selector
from parsel.xpathfuncs import set_xpathfunc
import unittest


class XPathFuncsTestCase(unittest.TestCase):
    def test_has_class_simple(self):
        body = u"""
        <p class="foo bar-baz">First</p>
        <p class="foo">Second</p>
        <p class="bar">Third</p>
        <p>Fourth</p>
        """
        sel = Selector(text=body)
        self.assertEqual(
            [x.extract() for x in sel.xpath('//p[has-class("foo")]/text()')],
            [u'First', u'Second'])
        self.assertEqual(
            [x.extract() for x in sel.xpath('//p[has-class("bar")]/text()')],
            [u'Third'])
        self.assertEqual(
            [x.extract() for x in sel.xpath('//p[has-class("foo","bar")]/text()')],
            [])
        self.assertEqual(
            [x.extract() for x in sel.xpath('//p[has-class("foo","bar-baz")]/text()')],
            [u'First'])

    def test_has_class_uppercase(self):
        body = u"""
        <p CLASS="foo">First</p>
        """
        sel = Selector(text=body)
        self.assertEqual(
            [x.extract() for x in sel.xpath('//p[has-class("foo")]/text()')],
            [u'First'])

    def test_set_xpathfunc(self):

        def myfunc(ctx):
            myfunc.call_count += 1

        myfunc.call_count = 0

        body = u"""
        <p CLASS="foo">First</p>
        """
        sel = Selector(text=body)
        self.assertRaisesRegexp(
            ValueError, 'Unregistered function in myfunc',
            sel.xpath, 'myfunc()')

        set_xpathfunc('myfunc', myfunc)
        sel.xpath('myfunc()')
        self.assertEqual(myfunc.call_count, 1)

        set_xpathfunc('myfunc', None)
        self.assertRaisesRegexp(
            ValueError, 'Unregistered function in myfunc',
            sel.xpath, 'myfunc()')
