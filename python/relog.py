#-*-coding:utf-8-*-
import sys, getopt,os,time

def usage():
	print("该脚本用于筛选一个大文件日志中，存在某段字符串的行，并输出结果到一个文件中.")
	print("您可以使用:[-i|-o|-s|-h] [--input|--output|--string|--help]")
	print("-i|--input 参数为需要处理日志文件")
	print("-o|--output 日志处理完后输入的文件，不填则在运行目录下生成")
	print("-s|--string 所包含的字符串")
	print("-h|--help 帮助信息")

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
	print("您输入的文件未找到!")
	sys.exit()
	
if (find_string == ""):
	print("-s|--string参数不能为空!")
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
print("共计 %d 行记录" % (line_count))
for index,line in enumerate(lines):
	print("进行 %d/%d" % (index + 1,line_count))
	if (line.find(find_string) != -1):
		fso_write.writelines(line)

fso_read.close()
fso_write.close()

print("操作已完成")