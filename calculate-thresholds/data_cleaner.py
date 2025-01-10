
def clean_xml_data(input_file, output_file):
    try:
        with open(input_file, 'r', encoding='utf-8') as infile:
            lines = infile.readlines()
        
        cleaned_data_lines = []
        
        # Add the XML declaration and root tag at the beginning
        cleaned_data_lines.append('<?xml version="1.0" encoding="UTF-8"?>\n')
        cleaned_data_lines.append('<records>\n')
        
        for line in lines:
            # Remove the unnessary prefix/suffix using regex
            if ':' in line:
                # Extract content appear after the second ":"
                line_content = line.split(":", 2)[-1].strip() # for sleep data

                # Ensure the quotes are straight (fix curly quotes or any potential encoding issues)
                line_content = line_content.replace("’", "'")  # Replace curly quotes with straight quotes for sleep data clean
                
                # Wrap the line content in a <Record> tag
                cleaned_data_lines.append(f'{line_content}</Record>\n') #uncomment this for sleep data and spo2 data
                # cleaned_data_lines.append(f'{line}</Record>\n') #uncomment this only for hb data 
        
        # Add the closing root tag at the end
        cleaned_data_lines.append('</records>\n')
        
        # Insert the cleaned lines to the output file
        with open(output_file, 'w', encoding='utf-8') as outfile:
            outfile.writelines(cleaned_data_lines)
        
        print(f"Cleaned XML has been written to {output_file}")
    
    except Exception as e:
        print(f"An error occurred: {e}")

# # # Specify the input and output file paths
input_xml = 'sleep_data/Sleep Analysis.xml'
output_xml = 'result_data/Cleaned_Sleep_Analysis.xml'

# input_xml = 'sleep_data/heart_rate.xml'
# output_xml = 'result_data/Cleaned_HB_Analysis.xml'

# input_xml = 'sleep_data/Spo2.xml'
# output_xml = 'result_data/Cleaned_SPO2_Analysis.xml'

# Run the function to clean and fix the XML
clean_xml_data(input_xml, output_xml)






