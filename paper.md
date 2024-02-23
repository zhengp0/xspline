---
title: 'xspline: A Python Package for Flexible Spline Modeling'

tags:
  - Python
  - Splines
  - Derivatives
  - Integrals 
  - Flexible Extraploation
  - Design matrix 

authors:
  - name: Peng Zheng
    orcid: 0000-0003-3313-215X
    affiliation: 1
- name: Kelsey Maass 
    orcid: 0000-0002-9534-8901
    affiliation: 1    
  - name: Aleksandr Aravkin
    orcid: 0000-0002-1875-1801
    affiliation: "1, 2"

affiliations:
 - name: Department of Health Metrics Sciences, University of Washington
   index: 1
 - name: Department of Applied Mathematics, University of Washington
   index: 2

date: 02.22.2024
bibliography: paper.bib

---

# Summary

Splines are a fundamental tool for describing and estimating nonlinear relationships [@de1978practical]. They allow nonlinear functions to be represented as linear combinations of spline basis elements. Researchers in physical, biological, and health sciences rely on spline models in conjunction with statistical software packages to fit and describe a vast range of nonlinear relationships. 

A wide range of tools and packages exist to support modeling with splines. These tools include 
- Splipy [https://pypi.org/project/Splipy/] [@johannessen2020splipy]
- splines [https://pypi.org/project/splines/]
- spline support in scipy [https://docs.scipy.org/doc/scipy/reference/generated/scipy.interpolate.BSpline.html]
- pyspline [https://mdolab-pyspline.readthedocs-hosted.com/en/latest/index.html]
- splinter [https://github.com/bgrimstad/splinter]  

Several important gaps remain in python packages for spline modeling.  `xspline` is not a comprehensive tool that generalizes existing software. Instead, it provides key functionality that undergirds flexible interpolation and fitting, closing existing gaps in the available tools.  `xspline` is currently widely used in global health applications [@murray2020global], undergidring the majority of spline modeling at the Institute of Health metrics and Evaluation (IHME).


# Statement of Need

Current spline packages offer broad functionality in spline fitting, including: 
- Manipulating and estimating curves (scipy, splines), surfaces and volumes (splipy, pySpline)
- Numerical derivatives (splipy, splines, scipy, pyspline, splinter)
- Interpolation (splipy, splines, scipy, pyspline, splinter)
- Spline derivatives, antiderivaties and numerical integrals (scipy)
- Extrapolation (scipy, limited)     

From this list, its apparent that `scipy` offers the most comprehensive features related to derivaties, integrals, and extrapolation. However, key limitations remain. First, while `scipy` provides derivative and anti-derivative spline objects, it still evaluates definite integrals numerically. In addition, while the first and last segments of the b-spline in `scipy` can be extrapolated, there is no option for the user to extrapolate a simpler functional form, e.g. a quadratic polynomial given a cubic spline. 

This functionality is essential to risk modeling. For example, data reported by all studies focusing on risk-outcome pairs are ratios of definite integrals across different exposure intervals. Prior packages do not offer a direct way to fit spline functions to these nonlinear data, because they do not provide definite integrals of splines as spline objects. Spline derivatives are also needed to impose shape constraints on risk curves of interest. Finally, extrapolations are often required to areas with little to no data, while maintaining high-fidelity fits for regions with dense data. Theoretically, it is straightforward to extrapolate any fit of degree less than or equal to the degree of the ultimate segments (for example, using slope matching for first order, slope and curvature for second order, etc.) However, this functinoality is not available in other packages. 


# Core idea and structure of `xpsline`

- Peng to write 

More information about the structure of the library can be found in [documentation](https://zhengp0.github.io/xspline/api_reference/), 
while the mathematical use cases are extensively discussed in [@zheng2021trimmed] and [@zheng2022burden] in the context of fitting risks. 


# Ongoing Research and Dissemination

The `xspline` package is widely used in all spline modeling done at IHME. In paricular, the new functionality described above enabled a new set of dose-response analyses recently published by the institue, including analyses of chewing tobacco [@gil2024health], education [@balaj2024effects], second-hand smoke [@flor2024health], intimate partner violence [@spencer2023health], smoking [@dai2022health], blood pressure [@razo2022effects], vegetable consumption [@stanaway2022health], and red meat consumption [@lescinsky2022health]. The results of all of these analyses are now publicly available at https://vizhub.healthdata.org/burden-of-proof/.  

# References
