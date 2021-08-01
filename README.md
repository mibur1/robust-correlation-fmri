## Robust Correlation for Link Definition in Resting-State fMRI Brain Networks

This repository contains a simple Python implementation of the "wrapping" method used in:

Burkhardt M, Giessing C, Thiel CM. 2021. Robust correlation for link definition in rs-fMRI brain networks\
can reduce motion-related artifacts. Brain Connect. DOI: 10.1089/brain.2020.1005.

**The method was first published in:**

Raymaekers J, Rousseeuw PJ. 2019. Fast robust correlation for high-dimensional data.\
Technometrics. DOI: 10.1080/00401706.2019.1677270. https://arxiv.org/abs/1712.05151.

and is also accessible through the cellWise R-toolbox:\
https://cran.r-project.org/web/packages/cellWise/index.html

### Usage:

The Python implementation uses the median and MAD to calculate the location and sale parameters. If you wish to use other options, please refer to the cellWise tooblox.
The data used for wrapping should be roughly Gaussian or at least symmetric in the center.

The main function is called wrap().

inputs:
* x: numpy array of data to be transformed through wrapping 
* params: one of three parameter sets used in the manuscript (possible values: 1,2,3)

returns:
*   Xw: transformed data
*   l: location
*   s: scale

Calling:

```
from wrapping import wrap
Xw, l, s = wrap(X, params=1)
```

is the Python equivalent of the following R code from the cellWise toolbox:

```
estX    <- estLocScale(X, type="wrapmedmad")
Xw      <- wrap(X, estX$loc, estX$scale)$Xw
```

### License:
This script is licensed under the GPLv3 License.
You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>
