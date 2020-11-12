# coding=utf-8
"""DockWidget test.

.. note:: This program is free software; you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by
     the Free Software Foundation; either version 2 of the License, or
     (at your option) any later version.

"""

__author__ = 'riccardo.klinger@gmail.com'
__date__ = '2020-11-12'
__copyright__ = 'Copyright 2020, Safegraph'

import unittest

from qgis.PyQt.QtGui import QDockWidget

from placekey_dockwidget import placekeyDockWidget

from utilities import get_qgis_app

QGIS_APP = get_qgis_app()


class placekeyDockWidgetTest(unittest.TestCase):
    """Test dockwidget works."""

    def setUp(self):
        """Runs before each test."""
        self.dockwidget = placekeyDockWidget(None)

    def tearDown(self):
        """Runs after each test."""
        self.dockwidget = None

    def test_dockwidget_ok(self):
        """Test we can click OK."""
        pass

if __name__ == "__main__":
    suite = unittest.makeSuite(placekeyDialogTest)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)

