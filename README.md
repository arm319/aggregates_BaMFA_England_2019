The study uses BaMFA methodology for reconciliation of the available data to quantify uncertainty and improve the reliability of the quantitative results.
This repository comprises input stocks and flows data ('.txt' files), model components, and the model runcode ('runaggregatemodel').
<br>
<br>

**System requirements**

The codebase was operated through the probabilistic programming library PyMC v5.10.3 and the Jupyter Notebook programming environment.
Python v3.11.7 was used.
<br>
<br>

**Python dependencies used:**

<li>pymc
<li>arviz
<li>pandas
<li>numpy
<li>math
<li>random
<li>matplotlib
<br>
<br>

**Coding environment**

The environment used to run the model through Conda is provided as a .yml file: 'BaMFA_Eng19_aggs.yml'
This contains all packages and dependencies in the versions employed in our case study, for increased repeatability.
<br>
To import to Conda: 
<li> Save the .yml file to the Conda directory/location you use 
<li> Run the following code in the terminal: conda env create -f BaMFA_Eng19_aggs.yml
<br>
  <br>
Run the following code in the terminal to view a list of your environments: conda info --envs
The environment 'BaMFA_Eng19_aggs' should be included.
<br>
  <br>
Guidance on creating a python environment from .yml files can be found at https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html
<br>
<br>

**Model runtime**

Runtime for the England (2019) dataset was approximately 40 minutes. This may vary. 
