# csv_donations
Use PICXTransformer_2022.py to convert PI Canada's monthly donor record in xlsx format, from January 2022 onward, into a user friendly format for the data converter at https://tnt.clcusa.org/
  1. Copy/Drag/Drop PICXTransformer_2022 into the folder you use for your records.
  2. Open your terminal, change to the folder you use for your records, run: python PICXTransformer_2022.py, 
          a) Alernatively if you have << Python Laucher >>
						installed (Win or Mac versions) right click 
            << PICXTransformer_2022.py >> and choose: 
            Open With --> Python Laucher to run the 
            program. (use Google to learn how to do these steps)
  3. You should now have a new csv file in your folder. Open https://tnt.clcusa.org/ in your browser
  4. Click << Browse >> and go to the folder and file this python program creates (parsed_'your employee ID number'_'report year and month'.csv) 
  5. Pick Pioneers Cananda as your Organization and Standard or Quickbooks as your file type. 
  6. Enter you employee ID number.
	7. Click << Convert >>
  7. Click << Download TntMPD file >> the output file. You will find this file in your Browser Downloads folder 
	
	The output file will be a tntdatasync file compatable for use at https://mpdx.org/ and on the old tntconnect v3.26.
 	For older monthly donor records (pre-October 2021) use csv_donationsv1-21.py for their conversion to a csv file ready for the data converter.

buy me a ☕ 😃 🥺?
