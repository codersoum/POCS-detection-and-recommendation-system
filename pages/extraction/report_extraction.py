from PyPDF2 import PdfReader
import re
#file_path=r'c:\\Users\\91950\\Downloads\\POCS_Report (15).pdf'
def parse_interpret(file_path):
    try :
        reader=PdfReader(file_path)
        rows= reader.pages[0].extract_text().splitlines()
        n=len(rows)
        i=0
        fixed=[]
        interpretations=[]
        while i<n-2:
            if re.match(r'^\d+(\.\d+)?$',rows[i+1]):
                fixed.append({
                    "parameter":rows[i],
                    "value":rows[i+1],
                    "normal_range":rows[i+2]
                })
                i+=3
            elif re.match(r'^[YN]$',rows[i+1]):
                fixed.append({
                    "parameter":rows[i],
                    "value":rows[i+1],
                    "normal_value":rows[i+2]
                })
                i+=3
            else:
                i+=1
        for item  in fixed:
            if "normal_range" in item:
                low,high=item["normal_range"].split("-")
                if float(item["value"].strip())<float(low.strip()):
                    status="Below normal"
                elif float(item["value"].strip())>float(high.strip()):
                    status="Above normal"
                else:
                    status="Within normal"
                interpretations.append(f"{item['parameter']} is {item['value']} which is {status} but normal range is {item['normal_range']}")
            else:
                if item["value"]==item["normal_value"][0]:
                    status="Normal"
                else:
                    status="Abnormal"
                interpretations.append(f"{item['parameter']} is {item['value']} which is {status} but normal value is {item['normal_value']}")
    except Exception as e:
        print (e)
        interpretations=[]
    finally:
         return interpretations
    


