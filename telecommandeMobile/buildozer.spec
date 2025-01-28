[app]
title = Leopard AI
package.name = leopardai
package.domain = com.turknovatech.leopardai
version = 0.1
source.dir = .
source.include_exts = py, kv, png, jpg, ttf, otf, webp
icon.filename = %(source.dir)s/icons/icon1.png
android.icon = %(source.dir)s/icons/icon1.png
android.presplash = %(source.dir)s/icons/icon2.png
requirements = python3, pyqt5, pyopengl, numpy
orientation = portrait
description = Une application PyQt pour Android.
android.arch = armeabi-v7a
android.api = 33
android.minapi = 23
android.sdk = 33
android.ndk = 23b
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE, ACCESS_NETWORK_STATE
android.opengl_es = 2
android.locales = en, fr, ar, tr
android.reduce_artifact = true
android.enable_compression = true
source.include_patterns = *.py, *.png, *.kv, *.webp
fullscreen = 0
android.allow_backup = true

[buildozer]
log_level = 3
debug = 1

[env]
