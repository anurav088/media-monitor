import csv
import xml.etree.ElementTree as ET

def csv_to_custom_xml(csv_file, xml_file, doc_value):
    # Create the root element for the XML structure
    root = ET.Element("recordSet")
    
    # Track the number of rows processed
    row_count = 0
    
    # Open and read the CSV file
    with open(csv_file, 'r') as f:
        reader = csv.DictReader(f)  # Automatically detects the header from the CSV
        
        # Iterate over each row in the CSV file
        for row in reader:
            # Create a record element for each CSV row
            record = ET.SubElement(root, "record")
            
            # Create the 'title' attribute and value
            attribute_title = ET.SubElement(record, "attribute", name="name")
            value_title = ET.SubElement(attribute_title, "value")
            value_title.text = row['directors_name']  # Fetch the 'Name' from CSV
            
            # Create the 'id' attribute and value
            attribute_id = ET.SubElement(record, "attribute", name="id")
            value_id = ET.SubElement(attribute_id, "value")
            value_id.text = row['din']  # Fetch the 'ID' from CSV
            
            # Create the 'doc' attribute and value
            attribute_doc = ET.SubElement(record, "attribute", name="doc")
            value_doc = ET.SubElement(attribute_doc, "value")
            value_doc.text = doc_value  # Use the common 'doc' value for all records
            
            # Increment the row count for every row processed
            row_count += 1
    
    # Write the generated XML to the output file
    tree = ET.ElementTree(root)
    tree.write(xml_file, encoding='utf-8', xml_declaration=True)
    
    # Compare the number of processed rows
    print(f"Processed {row_count} rows from CSV to XML.")
    
csv_file_path = '/Users/anandagarwal/Entity_resolution_Anirban /1000_directors.csv'  # CSV file path
xml_file_path = '/Users/anandagarwal/Entity_resolution_Anirban /1000_directors.xml'  # Desired XML file path
constant_doc_value = '1000_directors.csv'  # Common doc value for all entries

csv_to_custom_xml(csv_file_path, xml_file_path, constant_doc_value)