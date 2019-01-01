import os

if 'ANDROID_HOME' not in os.environ:
    print 'ANDROID_HOME not found!!!'
else:
    android_home = os.environ['ANDROID_HOME']
    
if 'ANDROID_NDK_HOME' not in os.environ:
    print 'ANDROID_NDK_HOME not found!!!'
else:
    android_ndk_home = os.environ['ANDROID_NDK_HOME']
