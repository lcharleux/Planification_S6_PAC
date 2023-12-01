# Automatic University Scheduling

Automatic planification of university courses. 

## Todo:

- Improve planification export with colors and autofilters.
- Add better optimisation criterions for soft constraints. The key would be to be able to create a stepwise function of the activity starting time for example to indicate the some activities fit better at givent times.
- Improve classes in order to simplify modelling.
- Remove JSON for teachers and students constraints an replace with simpler YAML for example.
- Investigate a bug that crashes the optimisation if teachers constraints overlap. 