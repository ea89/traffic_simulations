""" Imports an XML .net file and figures out what the roads are.
"""


import xml.etree.ElementTree as ET
import math
import sys
import shutil
from ParkingConstants import *



class MapXMLReader:

    def get_tree_and_root(self, filename):
        """
         This method parses the XML using xml.etree.ElementTree and then returns the root of the XML.
        :rtype: (ElementTree tree, Element root)
        :param filename: A relative path from the Python file
        :return: (ElementTree tree, Element root)
        """
        tree = ET.parse(filename)
        root = tree.getroot()
        return tree, root

    def make_node_map(self, node_root):
        """
        This method returns a dictionary from a String indicating a nodes name to its x and y coordinates. Note that for this
        method to work, nod.xml file has to be properly constructed
        :param node_root: The root of the nod.xml tree.
        :return: String name -> (double x, double y)
        """
        node_map = {}

        for child in node_root:
            node_map[child.get(NODE_ID)] = (float(child.get(X)), float(child.get(Y)))

        return node_map

    def __calculate_distance(self, from_id, to_id, node_map):
        return math.hypot(node_map[from_id][0] - node_map[to_id][0], node_map[from_id][1] - node_map[to_id][1])


    def __angle_of_lane(self,from_id, to_id):
        return math.atan2(self._node_map[to_id][1] - self._node_map[from_id][1], self._node_map[to_id][0] - self._node_map[from_id][0])

    def map_edge_length(self, node_map, edge_root):
        """
        This class takes in a node map (String name -> (double x, double y)), and the root of a edg.xml tree and then
        creates a map from the name of the edge to its length.
        :param node_map: String name -> (double x, double y)
        :param edge_root: Root of the edg.xml tree
        :return: String edge_name -> double length
        """
        edge_map = {}

        for child in edge_root:
            length = self.__calculate_distance(child.get(TO), child.get(FROM), node_map)
            edge_map[child.get(EDGE_ID)] = length

        return edge_map

    def __init__(self, pre):
        self._prefix = pre

        self._edge_tree, self._edge_root = self.get_tree_and_root('../%s.edg.xml' % self._prefix)
        self._node_tree, self._node_root = self.get_tree_and_root('../%s.nod.xml' % self._prefix)

        self._node_map = self.make_node_map(self._node_root)
        self._edge_length_map = self.map_edge_length(self._node_map, self._edge_root)

        pass

    def _get_all_edges(self):
        return self._edge_length_map.keys()

    def add_parking_spots(self, edge_ids = None, num_park_stops = sys.maxint, initial_l = L_INITIAL, end_l = L_END, theta = THETA, l_park = L_PARK, l_dist = L_DIST):
        """
        This is the method that adds parking spots to the lanes.
        :param edge_ids: Lanes to add the parking spot to (Default is all the edges
        :param num_park_stops: Number of parking spots to add; if no argument is passed in, it will default to adding as many as it can.
        :param initial_l: Leave the beginning of the lane blank by initial_l distance (default is L_INITIAL)
        :param end_l: Leave the beginning of the lane blank by end_l distance (default is L_END)
        :param theta: The angle in which the parking lane appears out (default is THETA)
        :param l_park: Length of the actual parking spot (default is L_PARK)
        :param l_dist: Length of the road leading to the parking spot (default is L_DIST)
        :return:
        """




        if edge_ids is None:
            edge_ids = self._get_all_edges()

        for child in self._edge_root:
            if child.get(EDGE_ID) in edge_ids:
                edge_id = child.get(EDGE_ID)

                current_point = self._node_map[child.get(FROM)]

                if (initial_l + end_l) >= self._edge_length_map[edge_id]:
                    continue

                #calculate slope for this lane
                from_id = child.get(FROM)
                to_id = child.get(TO)

                slope = self.__angle_of_lane(child.get(FROM), child.get(TO))

                #move forward by initial_l
                current_point = (current_point[0] + initial_l * math.cos(slope),
                                 current_point[1] + initial_l * math.sin(slope))

                #add parking spots recursively

                self.__add_recursive_parking_spots(current_point, self._node_map[to_id], num_park_stops, end_l, theta, l_park, l_dist, child, 1)

                self._node_tree.write("data/{}.nod.xml".format(self._prefix))
                self._edge_tree.write("data/{}.edg.xml".format(self._prefix))


    def __add_recursive_parking_spots(self, curr_pt, final_pt, num_park_stops, end_l, theta, l_park, l_dist, edge, count):

        #base case: check if there is any more room to add parking spots or parking spots left to add
        distance_until_end = math.hypot(curr_pt[0] - final_pt[0], curr_pt[1] - final_pt[1])
        distance_of_parking_and_endspace = end_l + 2*math.cos(theta) * l_dist + l_park
        if num_park_stops <= 0 or distance_until_end <= distance_of_parking_and_endspace:
            return

        #otherwise, add a new parking spot

        #1) add the first node away
        edge_id = edge.get(EDGE_ID)

        self._add_new_node(count, curr_pt, edge_id, PARKING_NODE_ONE_LABEL)

        #2) add the second node away

        slope = self.__angle_of_lane(edge.get(FROM), edge.get(TO))

        curr_pt = (curr_pt[0] + math.cos(theta + slope) * l_dist,
                   curr_pt[1] + math.sin(theta + slope) * l_dist)

        self._add_new_node(count, curr_pt, edge_id, PARKING_NODE_TWO_LABEL)

        #2) add the third node away

        curr_pt = (curr_pt[0] + math.cos(slope) * l_park,
                   curr_pt[1] + math.sin(slope) * l_park)

        self._add_new_node(count, curr_pt, edge_id, PARKING_NODE_THREE_LABEL)

        #4) finally add the fourth node

        curr_pt = (curr_pt[0] + math.cos(theta - slope) * l_dist,
                   curr_pt[1] - math.sin(theta - slope) * l_dist)

        self._add_new_node(count, curr_pt, edge_id, PARKING_NODE_FOUR_LABEL)

        #Now add all the lanes

        self._add_new_edge(count, edge_id, PARKING_NODE_ONE_LABEL, PARKING_EDGE_ONE_LABEL, PARKING_NODE_TWO_LABEL)
        self._add_new_edge(count, edge_id, PARKING_NODE_TWO_LABEL, PARKING_EDGE_TWO_LABEL, PARKING_NODE_THREE_LABEL)
        self._add_new_edge(count, edge_id, PARKING_NODE_THREE_LABEL, PARKING_EDGE_THREE_LABEL, PARKING_NODE_FOUR_LABEL)

        self.__add_recursive_parking_spots(curr_pt, final_pt, num_park_stops-1, end_l, theta, l_park, l_dist, edge, count+1)
        pass

    def _add_new_edge(self, count, edge_id, from_node, label, to_node):
        ET.SubElement(self._edge_root, EDGE_TAG, {EDGE_ID: '{}{}{}'.format(edge_id, label, count),
                                                  FROM: '{}{}{}'.format(edge_id, from_node, count),
                                                  TO: '{}{}{}'.format(edge_id, to_node, count),
                                                  PRIORITY_TAG: MAX_PRIORITY,
                                                  SPEED_TAG: SPEED,
                                                  NUM_LANES_TAG: NUM_LANES})

    def _add_new_node(self, count, curr_pt, edge_id, label):
        ET.SubElement(self._node_root, NODE_TAG, {NODE_ID: '{}{}{}'.format(edge_id, label, count),
                                                  X: '{}'.format(curr_pt[0]),
                                                  Y: '{}'.format(curr_pt[1]),
                                                  NODE_TYPE_TAG: NODE_TYPE})


if __name__ == '__main__':


    prefix = 'cross'
    self = MapXMLReader(prefix)

    self.add_parking_spots()


