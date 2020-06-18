import os

def AnalysisLineToFindInterface(file_path, line, save_path, version):
    start_pos = line.find('@interface')
    mid_pos = line.find(':')
    if(start_pos >= 0 and mid_pos >= 0):
        behind_line = line[mid_pos + 1: ]
        behind_line = "".join(behind_line.split())
        if behind_line[ : 2] == "id":
            behind_line = line[mid_pos + 1: ].strip()
            if behind_line.find(':') >= 0:
                #save_path.write(file_path + "\n")
                #save_path.write(line.strip() + "\n")
                behind_line = behind_line[behind_line.find(':') + 1: ].strip()
                if behind_line.find('(') >= 0:
                    behind_line = behind_line[: behind_line.find('(')]
                if behind_line.find('<') >= 0:
                    behind_line = behind_line[: behind_line.find('<')]
                if behind_line.find('{') >= 0:
                    behind_line = behind_line[: behind_line.find('{')]
                if behind_line.find(':') >= 0:
                    behind_line = behind_line[: behind_line.find(':')]
                if behind_line.find('\\') >= 0:
                    behind_line = behind_line[: behind_line.find('\\')]
                if behind_line.find('/') >= 0:
                    behind_line = behind_line[: behind_line.find('/')]
                if behind_line.find(' ') >= 0:
                    behind_line = behind_line[: behind_line.find(' ')]
                super_interface_name = behind_line.strip()
                line = line[start_pos + 10: ]
                if line.find('(') >= 0:
                    line = line[: line.find('(')]
                if line.find('<') >= 0:
                    line = line[: line.find('<')]
                if line.find('{') >= 0:
                    line = line[: line.find('{')]
                if line.find(':') >= 0:
                    line = line[: line.find(':')]
                if line.find('\\') >= 0:
                    line = line[: line.find('\\')]
                if line.find('/') >= 0:
                    line = line[: line.find('/')]
                interface_name = line.strip()
                save_path.write(interface_name.strip() + "\t" + super_interface_name.strip() + "\t" + version +"\n" + "\n")
        else:
            #save_path.write(file_path + "\n")
            #save_path.write(line.strip() + "\n")
            behind_line = line[mid_pos + 1: ].strip()
            if behind_line.find('(') >= 0:
                behind_line = behind_line[: behind_line.find('(')]
            if behind_line.find('<') >= 0:
                behind_line = behind_line[: behind_line.find('<')]
            if behind_line.find('{') >= 0:
                behind_line = behind_line[: behind_line.find('{')]
            if behind_line.find(':') >= 0:
                behind_line = behind_line[: behind_line.find(':')]
            if behind_line.find('\\') >= 0:
                behind_line = behind_line[: behind_line.find('\\')]
            if behind_line.find('/') >= 0:
                behind_line = behind_line[: behind_line.find('/')]
            if behind_line.find(' ') >= 0:
                behind_line = behind_line[: behind_line.find(' ')]
            super_interface_name = behind_line.strip()
            line = line[start_pos + 10: ]
            if line.find('(') >= 0:
                line = line[: line.find('(')]
            if line.find('<') >= 0:
                line = line[: line.find('<')]
            if line.find('{') >= 0:
                line = line[: line.find('{')]
            if line.find(':') >= 0:
                line = line[: line.find(':')]
            if line.find('\\') >= 0:
                line = line[: line.find('\\')]
            if line.find('/') >= 0:
                line = line[: line.find('/')]
            interface_name = line.strip()
            save_path.write(interface_name.strip() + "\t" + super_interface_name.strip() + "\t" + version +"\n" + "\n")

def GetTargetDescription(file_path, save_path, version):
	file = open(file_path, 'r')
	line = file.readline()
	target = '@interface'
	while line:
		if line.find(target) >= 0:
			AnalysisLineToFindInterface(file_path, line, save_path, version)
		line = file.readline()


def GetTargetFilePath(file_path, save_path, version):
	sub_paths = os.listdir(file_path)
	for sub_path in sub_paths:
		tmp_path = os.path.join(file_path, sub_path)
		if not os.path.isdir(tmp_path):
			if(tmp_path.endswith(".h") == 1):
				GetTargetDescription(tmp_path,save_path, version)
		else:
			GetTargetFilePath(tmp_path, save_path, version)


if __name__ == '__main__':
    root_filepath = "/Users/linjunhao/Desktop/complie_opt/sdk"
    version_filepaths = os.listdir(root_filepath)
    print ("interface:\n")
    for version_filepath in version_filepaths:
        target_filepath = os.path.join(root_filepath, version_filepath)
        if os.path.isdir(target_filepath):
            print (target_filepath)
            version_start = target_filepath.find('iPhoneOS')
            version_end = target_filepath.find('.sdk')
            version = target_filepath[version_start + 8 : version_end]
            save_name = "/Users/linjunhao/Desktop/complie_opt/TraversingOutput/interface/" + target_filepath[version_start : version_end] + "_interface.txt"
            fp = open(save_name, 'w')
            GetTargetFilePath(target_filepath, fp, version)
            fp.close()
		
