demo:
	python \
	demo0109.py \
	mnt/AN10102/HV2012.DAT \
	mnt/R301_2012/R301_CD2012.DAT \
	mnt/R301_2012/R301_OO2012.DAT \
	plots/demo0109.out.png
reformat:
	python \
	demo0113_2.py \
	data/hv.dat \
	mnt/ \
	drugs/drugnames4.txt \
	/home/LISM_lib/disk1/limin/IRfinal_project/data3  
reformat0116:
	python \
	demo0116.py \
	nouse \
	mnt/ \
	drugs/drugnames4.txt \
	/home/LISM_lib/disk1/limin/IRfinal_project/data4  
reformat0117:
	python \
	demo0117_2.py \
	nouse \
	mnt/ \
	drugs/drugnames4.txt \
	/home/LISM_lib/disk1/limin/IRfinal_project/data5  
	
ddtransit:
	python \
	demo0114.py \
	data/hv.dat \
	/home/LISM_lib/disk1/limin/IRfinal_project/data3 \
	ddt3.json
ddtransit0116:
	python \
	demo0116_2.py \
	nouse \
	/home/LISM_lib/disk1/limin/IRfinal_project/data4 \
	ddt4.json
#cancer drug barchart #revision piechart
cdb:
	python \
	demo0117.py \
	drugs/drugnames4.txt \
	/home/LISM_lib/disk1/limin/IRfinal_project/data4 \
	demo0117.out \
	plots 
#drug status piechart
dsp:
	python \
	demo0118.py \
	drugs/drugnames4.txt \
	/home/LISM_lib/disk1/limin/IRfinal_project/data4 \
	demo0118.out \
	plots \
	IDOUT.json
#drug status piechart
dsp2:
	python \
	demo0118_2.py \
	drugs/drugnames4.txt \
	/home/LISM_lib/disk1/limin/IRfinal_project/data5 \
	demo0118_2.out \
	plots \
	IDOUT.json
