# EarthqWaze
This is a software solution that aids disaster response teams by identifying optimal terrestrial routes through calamity-stricken areas. It uses satellite image data to assess road condition and detect obstruction.

## Summary
There are four stages in the pipeline of this project:
* Converting images into matrices and masking them with different levels of obstruction.
* Visual Recognition training through IBM Cloud to distinguish between masked and unmasked images (how bad road conditions are).
* Assigning weights to each edge, which consists of two nodes, where each node exists around the center of a unit of the smallest image block.
* Running a generic shortest-path algorithm (not A-star) on the graph generated in the previous stage and using the output to visualize a styled graph and produce a route on a map.

## Contributors
Current: Nico Deshler, Billy Chau, Sam Wu, Justin Wong.

## Next Steps
We hope to improve the front-end implementation of this project and provide better UI experience by allowing the user to input the starting location and the destination on a map (i.e. an interactive map).
