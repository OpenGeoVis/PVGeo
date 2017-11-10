# PVGPpy
PVGPpy is a python module we are developing for direct use of our macros in the ParaView shell. This module will contain all of our macros for your use. We are publishing our macros in this manner to:

1. Streamline their use by allowing users to call the macros like python functions directly from the ParaView shell.
2. Easily update/change the macros without constant merge conflictions as users will need to input certain parameters for their use. This is much easily done through function calls than overwriting the macro files.

More details to come... In a nut shell, add the `import_PVGPpy.py` macro to ParaView and use this have the module imported for your use.
