"""
This package is designed to convert a regular network into one that has parking spots on its lanes. To use this package,
 just import it and then call ParkingGeneratorMain's update_network(edge_network_name) method. It expects the
 correct path name to the edg.xml file. Once that is given, it will spit out a network with the parking nodes. Additional
 settings may be changed by editing the text file within the package. Alternatively, an optional second argument may be
 passed in to the update_network() method to pull the optional text file instead. (Useful for dynamically generated
 parameters)
"""