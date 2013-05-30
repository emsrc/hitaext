#!/usr/bin/env python

"""
distutils setup script for distributing the Hitaext
"""

from sys import argv
from glob import glob
from os import system


long_description="""
Hitaext is a tool for manually aligning arbitraty text spans from two arbitrary XML documents
"""

version = "1.0"
name = "hitaext"
mainscript = "bin/%s.py" % name

# clean dist and MANIFEST
system("rm -rfv MANIFEST build")


if "py2app" in argv:
    # ============================================================
    # Mac OS X binary package
    # ============================================================
    # - py2app crashes if the main script has no .py extension!
    #   (TypeError: Don't know how to handle ...ls bi)
    # - py2app stable version has problem with ElementTree
    #   see http://mail.python.org/pipermail/pythonmac-sig/2007-February/018673.html
    #   so you need to upgrade modulegraph ("easy_install-2.5 modulegraph==dev")
    # - py2app requiqres setuptools
    from setuptools import setup
    
    base_resources = ["README", "INSTALL", "COPYING","CHANGES"]
    resources = base_resources + glob("doc/*")
    
    py2app_options = dict(
        # Cross-platform applications generally expect sys.argv to
        # be used for opening files.
        argv_emulation=True,
        resources=resources,
        dist_dir="dist-py2app")
    
    extra_options = dict(
        setup_requires=['py2app'],
        app=[mainscript],
        packages=["htxt"],
        platforms="Mac OS X",
        options=dict(py2app=py2app_options),
    )
    
elif "py2exe" in argv:
    # ============================================================
    # Windows binary package
    # ============================================================
    from distutils.core import setup
    import py2exe
    
    # ElementTree is not automatically included in the dependencies,
    # so we have to add it explictly
    py2exe_options = dict(
        includes = ["xml.etree.ElementTree"] )
    
    extra_options = dict(
        setup_requires = ['py2exe'],
        windows = [mainscript],
        packages=["htxt"],
        platforms = "Windows",
        options=dict(
            py2exe=py2exe_options))
elif "bdist_rpm" in argv:
    # ============================================================
    # RPM
    # ============================================================
    from distutils.core import setup
    from os import mkdir

    mkdir("dist-rpm")
    
    bdist_rpm_options = dict( 
        dist_dir="dist-rpm")
    
    extra_options = dict(
        scripts=[mainscript],
        # sdist does not automatically resolve the dependency on part of the daeso,
        # so we explicitly add daeso.ptc
        # this requires a symlink
        packages=["htxt", "daeso.ptc"],
        requires=["wx"],
        provides=["htxt (%s)" % version],
        platforms="RPM-based Linux",
        options = dict(
            bdist=bdist_rpm_options))
else:
    # ============================================================
    # source
    # ============================================================
    from distutils.core import setup
    
    sdist_options = dict( 
        dist_dir="dist-sdist",
        formats=["zip","gztar","bztar"],)
    
    extra_options = dict(
        # Normally unix-like platforms will use "setup.py install"
        # and install the main script as such
        scripts=[mainscript],
        packages=["htxt"],
        requires=["daeso", "wx"],
        provides=["htxt (%s)" % version],
        platforms="POSIX, MacOS X, Windows",
        options = dict(
            sdist=sdist_options))


setup(name="hitaext",
      version=version,
      description="HITAEXT: Hierachical Text Alignment Tool",
      long_description=long_description,
      author="Erwin Marsi",
      author_email="e.marsi@gmail.com",
      url="https://github.com/emsrc/hitaext",
      package_dir={"": "lib"},
      license="GNU Public License",
      **extra_options)



if "py2app" in argv:
    # ============================================================
    # Mac OS X postinstallation
    # ============================================================
    from shutil import copytree
    
    img_name = name + "-" + version
    print "img_name:", img_name
    
    # create disk image
    system("rm -f dist-py2app/%s.dmg" % img_name)
    system("hdiutil create -size 65M -fs HFS+ -volname %s dist-py2app/%s" % (img_name, img_name))
    system("hdiutil mount dist-py2app/%s.dmg" % img_name)
    system("cp -rv dist-py2app/%s.app /Volumes/%s" % (name, img_name))
    
    for fn in base_resources:
        system("cp -v %s /Volumes/%s" % (fn, img_name))
        
    system("cp -rv doc /Volumes/" + img_name)
    system("cp -rv data /Volumes/" + img_name)
    # get rid of .svn dirs
    system('find /Volumes/%s -type d -name ".svn" -exec rm -rf {} \;' % img_name)
    
    system("hdiutil unmount /Volumes/%s" % img_name)
    
    system("cd dist-py2app && zip %s.dmg.zip %s.dmg" % (img_name, img_name))
elif "py2exe" in argv:
    # ============================================================
    # MS Windows  postinstallation
    # ============================================================
    # TODO: this can be done automatically
    print "Now run check the setup in iss\\hitaext.iss"
    print "(version number, required files, etc)"
    print "and run Inno Setup Compiler to create a setup.exe" 
    
    
