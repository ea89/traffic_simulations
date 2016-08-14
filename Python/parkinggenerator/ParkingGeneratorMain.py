"""
Main method for this package; it is the class that calls onto the class to read the XML, and then starts creating the two new
xml files
"""

import xml.etree.ElementTree as ET

tree = ET.parse('country_data.xml')
root = tree.getroot()

