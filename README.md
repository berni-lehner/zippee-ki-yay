# zippee-ki-yay
The zippee-ki-yay module provides the Python interfaces to extract namelist from a zip archive without the need to download it first.

[Bernhard Lehner](https://www.researchgate.net/profile/Bernhard_Lehner)


# Example
    $ from zippeekiyay import namelist

    $ url = r"https://zenodo.org/record/5205460/files/ASPAI.zip"
    $ flist = namelist(url)
    $ print(flist)

## output
`
['ASPAI/', 'ASPAI/full_range/', 'ASPAI/full_range/ensemble/', 'ASPAI/full_range/ensemble/mse_losses.pkl', 'ASPAI/full_range/ensemble/results.pkl', 'ASPAI/full_range/ensemble/uncertainties_ens.pkl', 'ASPAI/full_range/single_model/', 'ASPAI/full_range/single_model/mse_losses.pkl', 'ASPAI/full_range/single_model/uncertainties_area.pkl', 'ASPAI/full_range/single_model/uncertainties_org.pkl', 'ASPAI/high_range/', 'ASPAI/high_range/ensemble/', 'ASPAI/high_range/ensemble/mse_losses.pkl', 'ASPAI/high_range/ensemble/results.pkl', 'ASPAI/high_range/ensemble/uncertainties_ens.pkl', 'ASPAI/high_range/single_model/', 'ASPAI/high_range/single_model/mse_losses.pkl', 'ASPAI/high_range/single_model/uncertainties_area.pkl', 'ASPAI/high_range/single_model/uncertainties_org.pkl', 'ASPAI/readme.txt']
`


# Installation
## Requirements and Dependencies
- Ubuntu (tested with 19.10) or Windows 10 Pro (tested with Version 1903 for x64)
- Python (tested with Python = 3.7 in Anaconda = 4.8.3)
- io, struct, requests, zipfile, pathlib



# Acknowledgements
for inspiration goes to https://betterprogramming.pub/how-to-know-zip-content-without-downloading-it-87a5b30be20a

# Contact

[Bernhard Lehner](mailto:berni.lehner@gmail.com)
