# WhiteboxTools

In order to make WhiteboxTools (an open source hydrological analysis program) available to the WALLY API, we will build a copy of the whitebox_tools executuable and thie whitebox_tools Python bindings in this container.

The WALLY backend API buildconfig can then copy those two artifacts into its own container.

The WhiteboxTools image does not need to be rebuilt unless upgrading WhiteboxTools.

https://jblindsay.github.io/ghrg/WhiteboxTools/index.html
