series{
    file = $dat_file
    period = $period
    format = Datevalue
}
spectrum{
    savelog = peaks
    print = none
}
transform{
    function = auto
}
regression{
    variables = ()
    aictest = ( td easter )
    savelog = aictest
    print = none
}
outlier{
    types = ( $outliers )
}
automdl{
    savelog = amd
    print = none
}
forecast{
    maxlead = 4
    print = none
}
estimate{
    maxiter = 3000
    print = none
    savelog = (aicc aic bic hq afc)
}
check{
    print = none
    savelog = (lbq nrm)
}
x11{
    seasonalma = MSR
    savelog = all
    save = seasadj
    print = ( none +d11 )
}
slidingspans{
    print = none
    savelog = percent
    additivesa = percent
}
history{
    estimates = (fcst aic sadj sadjchng trend trendchng)
    savelog = (asa ach atr atc)
    print = none
}
