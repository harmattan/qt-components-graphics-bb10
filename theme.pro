TEMPLATE = subdirs

# here we allow for setting of an install prefix:
#
# 1. if the PREFIX command line parameter is given like this:
#        qmake PREFIX=/usr/local/
#    then use it, else
# 2. if meegotouch_defines.prf can be found, use it, else
# 3. default to /usr/

!isEmpty( PREFIX ) {
    THEME_DIR = $$PREFIX/share/themes
} else {
    exists( $$[QMAKE_MKSPECS]/features/meegotouch_defines.prf ) {
        load(meegotouch_defines)
        THEME_DIR = $$M_THEME_DIR
    } else {
        THEME_DIR = /usr/share/themes
    }
}

# BASE THEME
base.files = ./base
base.path = $$THEME_DIR
base.CONFIG += no_check_exist

INSTALLS += base \

QMAKE_CLEAN += build-stamp configure-stamp
QMAKE_DISTCLEAN += build-stamp configure-stamp
