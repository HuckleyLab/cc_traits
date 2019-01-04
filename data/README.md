Four datasets were used in this analysis, as follows:

[angert11]: http://doi.wiley.com/10.1111/j.1461-0248.2011.01620.x
[pinsky13]: http://science.sciencemag.org/content/341/6151/1239
[rumpf18]: http://www.pnas.org/content/115/8/1848

* **Swiss Alpine Plants** (*from [Angert et al, 2011][angert11]*): historic elevational range shifts of alpine plant species.
* **European Plants** (*from [Rumpf et al, 2018][rumpf18]*): historic elevational range shifts of european plant species.
* **Marine Fish** (*from [Pinsky et al, 2013][pinsky13]*): historic latitudinal range shifts of marine fishes.
* **Western North American Mammals** (*from [Angert et al, 2011][angert11]*): historic elevational range shifts of small mammals in Yosemite National Park, CA, USA.

## Traits

**Data Sources**: All datasets except for **Marine Fish** had traits already incorporated in them from their original publications. Our marine dataset merges [Pinsky's][pinsky13] original range shift data with [FishBase](http://www.fishbase.org) trait data. This merger is performed in `/code/R/trawl-shifts.R`.

**Trait Descriptions**: Within each dataset folder find a `traits-desc-{dataset-name}.csv` file, which gives English trait descriptions to variable names where available. These `traits-desc` files are used in plotting (see `/code/0-Nonlinear-Trait-Modeling.ipynb`).

---
<img align="center" src="../huckleylab-footer.png">
