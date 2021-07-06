# pyctf
Open a CTF MEG dataset:

    from pyctf import dsopen

    ds = dsopen("dataset.ds")

Return a numpy array of MEG data from trial 0:

    data = ds.getPriArray(0)
