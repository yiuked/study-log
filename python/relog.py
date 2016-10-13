#-*-coding:utf-8-*-
import sys, getopt,os,time

def usage():
	print("�ýű�����ɸѡһ�����ļ���־�У�����ĳ���ַ������У�����������һ���ļ���.")
	print("������ʹ��:[-i|-o|-s|-h] [--input|--output|--string|--help]")
	print("-i|--input ����Ϊ��Ҫ������־�ļ�")
	print("-o|--output ��־�������������ļ���������������Ŀ¼������")
	print("-s|--string ���������ַ���")
	print("-h|--help ������Ϣ")

opts, args = getopt.getopt(sys.argv[1:], "hi:o:s:")
input_file = ""
output_file = ""
find_string = ""

for op, value in opts:
	if (op in ("-i", "--input")):
		input_file = value.strip()
	elif op in ("-o", "--output"):
		output_file = value.strip()
	elif op in ("-s", "--string"):
		find_string = value.strip()
	elif op in ("-h", "--help"):
		usage()
		sys.exit()

if (os.path.exists(input_file) == False):
	print("��������ļ�δ�ҵ�!")
	sys.exit()
	
if (find_string == ""):
	print("-s|--string��������Ϊ��!")
	sys.exit()


if (output_file == ""):
	output_file = os.getcwd() + "\\" + str(int(time.time())) + ".log"

if (os.path.exists(output_file) == False):
	new_dir = os.path.dirname(output_file)
	if (os.path.exists(new_dir) == False):
		os.makedirs(os.path.dirname(new_dir))

fso_read = open(input_file, 'r')
fso_write = open(output_file, 'w')
lines = fso_read.readlines()

line_count = len(lines)
print("���� %d �м�¼" % (line_count))
for index,line in enumerate(lines):
	print("���� %d/%d" % (index + 1,line_count))
	if (line.find(find_string) != -1):
		fso_write.writelines(line)

fso_read.close()
fso_write.close()

print("���������")