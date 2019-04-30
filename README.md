# EarthqWaze
This is a software solution that aids first responders by identifying optimal terrestrial routes through disaster-stricken areas. It uses satellite image data to assess road conditions and detect obstruction.

## Summary
There are four stages in the pipeline of this project:
* Isolating road networks in satellite images of disaster-stricken areas using image processing techniques and Google Maps Static API.
* Training a computer vision model using IBM Cloud's Visual Recognition service to classify the condition of different road segments after a disaster.
* Generating an undirected graph from the learned road quality classifications of the affected region. The edge weights of this graph are assigned based on the amount of damage sustained to different sub-networks during a calamity. 
* Running a generic least-time path algorithm on the graph generated in the previous stage. Outputs include a stylized graph representing the conditions of roads in different parts of the search region and a Google Maps image highlighting the optimal path from a provided start location and destination.

## Parameter Information
The pipeline accepts two pairs of latitude and longitude coordinates (the starting location and the destination of the user) as input and returns two visual aids for outputs. The first is a roadmap highlighting the least-time optimal route from the starting location to the destination displayed in the format of Google Maps. The second is a stylized graph that represents which road networks in the search space have been most affected. This macroscopic information of the broader region could help teams identify areas that are most urgently in need of aid.

## Dependencies
To run GMaps_DSet_Gen.py you will to pip install the following packages:
* matplotlib
* requests
* polyline
* numpy
* networkx
* webbrowser
* Pillow
* urllib

#Additionally, you will need to provide an google cloud api key that enables Google Maps and Roads APIs

## Contributors
Current: Nico Deshler, Billy Chau, Sam Wu, Justin Wong.

## Next Steps
We hope to improve the front-end implementation of this project and provide better UI experience by allowing the user to input the starting location and the destination on a map (i.e. an interactive map) using their mobile devices. We also hope to improve how we generate simulated training datasets to make our computer vision model more robust to a broader array of natural disasters. Finally we hope to include a safest-path feature using the same satellite data to support evacuees.

## Additional Use Cases 
This package could also potentially serve as a monitoring system for road networks around the globe and inform on potential hazards.
