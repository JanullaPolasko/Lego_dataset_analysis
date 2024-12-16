import subprocess

#create db and insert it with data from excel
subprocess.run(["python", "create_tables.py"])
subprocess.run(["python", "insert_data.py"])

#cleaning (maybe not needed at this point cause excel is already cleaned
subprocess.run(["python", "cleaning.py"])

#crawling website about actual information
subprocess.run(["python", "get_prices.py"])
subprocess.run(["python", "get_status.py"])
subprocess.run(["python", "get_pictures.py"])

subprocess.run(["python", "get_info.py"])

#updating excel file
subprocess.run(["python", "data_to_excel.py"])
