from collections import defaultdict
import os


Input_FilePath  = '/staging/reserve/aging/chia2831/FabryDisease/Fabry_Data_93/recode_vcf/'
Output_FilePath = '/staging/reserve/aging/chia2831/FabryDisease/Fabry_Data_93/Variant_QC_result/'
os.system('[ ! -d {} ] && mkdir -p {}'.format(Output_FilePath, Output_FilePath))

Amount_of_Samples = '93'
VCF_samplelist = '{}_recode_vcf_samplelist.txt'.format(Amount_of_Samples)
os.system('ls {} > {}{}'.format(Input_FilePath, Output_FilePath, VCF_samplelist))


def Judge_TypesOfGeneticVariation(line_list):
	CHROM, POS, ID, REF, ALT = line_list[0:5]
	if (len(REF) == len(ALT)) and (len(REF) == 1) and (len(ALT) == 1):
		return 'SNV'
	elif (len(REF) == len(ALT)) and (len(REF) > 1) and (len(ALT) > 1) and (',' in ALT):
		return 'Deletion'
	elif len(REF) > len(ALT):
		return 'Deletion'
	elif len(REF) < len(ALT):
		return 'Insertion'
	else:
		return 'others'

# 計算 Variant QC
with open(Output_FilePath + VCF_samplelist, 'r') as f:
	VCF_samplelist = f.readlines()

# Write "SNV, Deletion, Insertion" in one file
Output_report_txt = 'SNV_Deletion_Insertion_{}_report.txt'.format(Amount_of_Samples)
f_out_report = open(Output_FilePath + Output_report_txt, 'w')


# Dictionary ==> SampleID : {'CNV': 700, 'Deletion': 200, 'Insertion': 300, 'others': 50}
CNV_Del_Ins_dict = defaultdict(lambda: defaultdict(lambda: 0))

for vcf_file in VCF_samplelist:
	vcf_file = vcf_file.strip()

	with open(Input_FilePath + vcf_file, 'r') as f_in:
		line = f_in.readline()
		while line != '':
			if line.startswith('#'):
				pass
			else:
				try:
					line_list = line.split('\t')
					VariantsType = Judge_TypesOfGeneticVariation(line_list)
					#print(line_list[0:5], '【', VariantsType, '】')
					if VariantsType == 'SNV':
						CNV_Del_Ins_dict[vcf_file]['SNV'] += 1
					elif VariantsType == 'Deletion':
						CNV_Del_Ins_dict[vcf_file]['Deletion'] += 1
					elif VariantsType == 'Insertion':
						CNV_Del_Ins_dict[vcf_file]['Insertion'] += 1
					elif VariantsType == 'others':
						CNV_Del_Ins_dict[vcf_file]['others'] += 1
					else:
						print(line_list[0:5])
				except:
					print('can not split =>', line)
			line = f_in.readline()


f_out_report.write('SampleID\tSNV\tDeletion\tInsertion\tothers\n')
for SampleID in CNV_Del_Ins_dict.keys():
	f_out_report.write('{}\t{}\t{}\t{}\t{}\n'.format(SampleID, CNV_Del_Ins_dict[SampleID]['SNV'], CNV_Del_Ins_dict[SampleID]['Deletion'], CNV_Del_Ins_dict[SampleID]['Insertion'], CNV_Del_Ins_dict[SampleID]['others']))
f_out_report.close()
