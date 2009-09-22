from distutils.core import setup
files = ["NTV/*"]

setup(name = "NTV",
version="0.2",
description="Astronomical Data Viewer",
author="Nate Lust",
author_email="nlust@physics.ucf.edu",
packages=['NTV'],
requires=['numpy','matplotlib','pyfits','PyQt4','scipy'],
license="revised BSD",
scripts=['ntv'])
