# Notes on the copper sample from USGS

The copper concentration data provides interesting results. The min value fround was 0.25 mg/kg while the max was 996 mg/kg, which is an extreme outlier. The mean value was 17.94 mg/kg. When trying to plot these values in a histogram each bin would have to be very small, as 75% of the data sits under 20.90 mg/kg. Thus, we use a log base 10 graph to make the bin size more meaningful with the small values. None of the values are 0 or negative, so the logarithmic conversion will not fail.

One thing to note is that values under the detection threshold have been halved, so there might be a spike around the low end of the graph.
