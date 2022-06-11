# MetricMeter
A package for which handling the trend of metrics while training a deep learning model, such as the trend of loss, accuracy, f1-score in each epoch or iteration etc.

## Version
*v0.0.1*
## Modules
### **Tracker**
`Tracker` is the core module which used for recording and summarizing the time series, such as running mean `AverageTracker` or running variance `VarTracker`.

For example, we can `append` the loss of each batch and `get` the running mean of loss. Concluded, the aim of `Tracker` is tracking the running metric in a single iteration.

### **Meter**
`Tracker` handles the running metric of each iteration, while `Meter` collects the final metric of `Tracker` in each epoch. 

For example, after all iterations is over, `Meter` saves the mean of loss in this iteration, resets `Tracker` and goes forward to the next epoch.

## Note
:warning: The repository is heavily under constructing, thus welcome to provide any inspiration or thought, even make contributions!