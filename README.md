# MSc thesis codes: "Catching GRBs from a different point of view: the case of EP240414a".
## Author: Eduardo González Ramos
## Supervisors: Maria E. Ravasio and Peter G. Jonker
## Master in Particles and Astrophysics / Astrophysics Department / Radboud University

On this website, you can find all the codes used in Python to obtain the MSc thesis results and figures. The notebooks are ordered by numbers following the same order as they were employed to discuss the different chapters and sections in the thesis, i.e., from 1 to 8. In this way, each notebook contains:

**Notebook 1:** In this notebook, we study the typical GRB afterglow emission by coding an interactive plot in which we can change different values of the afterglow model parameters such as the viewing angle or the density of the environment. Furthermore, it also includes different analytical expressions for computing the times of expected breaks in the light curve for the GRB afterglow observed on-axis. The code was programmed using a Jupyter notebook in Visual Studio Code editor. Therefore, the interactive figure should work under these conditions.

**Notebook 2:** In this notebook, we study the suppression factor in the prompt emission observed quantities $E_{iso}$ and $F_{\Delta \nu}$ due to the viewing angle effect. We refer the reader to the thesis to understand the procedure and codes included in this notebook.

**Notebook 3:** In this notebook, we combine the knowledge gained from the previous two notebooks to deduce the unified afterglow and prompt methodology described in the MSc thesis. The results of both notebooks are combined through the introduction of the radiative efficiency parameter, and the resulting combination is illustrated following the interactive figure with modifiable parameters initially coded in Notebook 1. The code was programmed using a Jupyter notebook in Visual Studio Code editor. Therefore, the interactive figure should work under these conditions. In this notebook it is assumed only a top-hat jet.

**Notebook 4:** Same as above, but this time assuming a Gaussian structured jet.

**Notebook 5:** Notebook coded for extracting the publicly available EP240414a data in different magnitudes and for reducing and 'cleaning' it following the procedure described in the thesis. The input of this notebook is the .txt files included in the folder 'EP240414a Data from different articles' and the output is the ones included in the folder 'EP240414a Edu processed data'. In the latter, the EP240414a multiwavelength data is in flux densities, and 'cleaned' and ready to be fitted by different models in the fitting process. Note that the content of this folder is also presented in the Appendix B of the thesis. Moreover, in the code that processes the X-ray data, a consistency test is performed to verify that it is functioning properly. This test is conducted using the data for the GRB 251005C, contained in folder 'GRB 251005C data to check codes'. For this example event, the data is obtained from the Swift X-ray Observatory website, where the positive result of this test is also verified.

**Folder 6:** This folder contains the notebooks used to perform the fit of different models to the processed EP240414a data. Therefore, the input of these notebooks is the folder 'EP240414a Edu processed data' and the output is created when running this code inside the folder as fitting results for an specific dataset and model. There are also two notebooks included for analyzing these fitting results, which therefore need as input the files obtained from the previous notebooks. Inside this folder, I am also uploading the final results of the fit described in the thesis. However, intermmediate results are not uploaded due to their large file size and the large number of files, but can be easily obtained by modifications of the notebooks performing the fits and following the procedure described in the thesis. Lastly, in this folder, one can also find the custom data likelihood function defined for the fitting process (see MSc thesis). $^1$

**Notebook 7:** This notebook contains the codes used to perform the SED analysis of the Phase 1 multiwavlength data from photometric data points. We refer the reader to the thesis to understand all the steps taken in this notebook and the reason for its existence. $^1$

**Notebook 8:** This notebook contains the codes used to calculate the suppression factor of the EP240414a prompt emission from the final fitting results of the afterglow + arnett model to the light curve. Moreover, it also discusses the lack of gamma-rays detected, the jet environment nature inferred from the fitting, and the EP240414a on-axis corrected prompt emission in the context of LGRBs empirical correlations. This is the notebook on which the final section of the results chapter and the discussion chapter are based. $^1$

$^1$ *NOTE OF THE CURRENT VERSION*: Unfortunately, these notebooks are not presented and explained as the author would like due to a lack of time. Therefore, althought the codes work perfectly, they were the ones used to obtain the thesis results and the reader can find comments in them, the code may not be fully understood due to a lack of explanations for each step. I apologize for the inconvenience, and updates with explanations for each step will be added as soon as possible.


Finally, I would like to thank the reader for taking the time to use these codes. I would be very grateful if you would contact me if you do not understand something about the codes, if there are any errors in them, or if you have any comments about them. 
Thank you a lot for your time and help.

Yours sincerely,
Eduardo