import os
import linecache
import re


def GetPropertyDefinition(line, save_path, interface_name, line_count):
	if line.find(';') >= 0:
		save_path.write(str(line_count) + "----" + line + "\n" )

def GetProperty(line, save_path, interface_name, version, line_count):
    if line.find(';') >= 0:
    	#save_path.write(str(line_count) + "----" + line + "\n" )
        property_start_pos = line.find('@property')
        property_end_pos = line.find(';')
        definition_str = ""
        if (line[property_start_pos + 9] != "(" and line[property_start_pos + 10] != "(" and line[property_start_pos + 11] != "(" and line[property_start_pos + 12] != "("):
            definition_str = line[property_start_pos + 9: property_end_pos]
        else:
            definition_str = line[line.find(')') + 1: property_end_pos]
        if definition_str.find('__OSX_') >= 0:
            definition_str = definition_str[: definition_str.find('__OSX_')]
        if definition_str.find('__IOS_') >= 0:
            definition_str = definition_str[: definition_str.find('__IOS_')]
        if definition_str.find('__API_') >= 0:
            definition_str = definition_str[: definition_str.find('__API_')]
        if definition_str.find('__WATCHOS_') >= 0:
            definition_str = definition_str[: definition_str.find('__WATCHOS_')]
        if definition_str.find('__TVOS_') >= 0:
            definition_str = definition_str[: definition_str.find('__TVOS_')]
        if definition_str.find('API_') >= 0:
            definition_str = definition_str[: definition_str.find('API_')]
        if definition_str.find('WK_') >= 0:
            definition_str = definition_str[: definition_str.find('WK_')]
        if definition_str.find('MPS_') >= 0:
            definition_str = definition_str[: definition_str.find('MPS_')]
        if definition_str.find('MP_') >= 0:
            definition_str = definition_str[: definition_str.find('MP_')]
        if definition_str.find('UI_') >= 0:
            definition_str = definition_str[: definition_str.find('UI_')]
        if definition_str.find('UIKIT_') >= 0:
            definition_str = definition_str[: definition_str.find('UIKIT_')]
        if definition_str.find('PDFKIT_') >= 0:
            definition_str = definition_str[: definition_str.find('PDFKIT_')]
        if definition_str.find('CS_') >= 0:
            definition_str = definition_str[: definition_str.find('CS_')]
        if definition_str.find('PHOTOS_') >= 0:
            definition_str = definition_str[: definition_str.find('PHOTOS_')]
        if definition_str.find('NS_') >= 0:
            definition_str = definition_str[ : definition_str.find('NS_')]
        if definition_str.find('HK_') >= 0:
            definition_str = definition_str[ : definition_str.find('HK_')]
        if definition_str.find('CA_') >= 0:
            definition_str = definition_str[ : definition_str.find('CA_')]

        definition_str = definition_str.strip()
        if(definition_str.find("/*") >= 0):
            definition_str = definition_str[ : definition_str.find("/*")]
        definition_str = definition_str.strip()
        special_pos = definition_str.find('^')
        is_special_property = 0
        if special_pos >= 0:
            tmp_pos_start = definition_str.rfind('<', 0, special_pos)
            if tmp_pos_start == -1:
                is_special_property = 1
        if re.search('(.*?)\((.*?)\^(.*?)\)(.*?)\((.*?)\)(.*?)(.*?)',definition_str) and is_special_property == 1:
            ls = re.search('(.*?)\((.*?)\^(.*?)\)(.*?)\((.*?)\)(.*?)(.*?)',definition_str)
            type_name = ls.group(1) + "(^)(" + definition_str[definition_str.rfind(ls.group(5)): ]
            self_name = ls.group(3)
            type_name = "".join(type_name.split())
            self_name = "".join(self_name.split())
            save_path.write(type_name + "\t" + self_name + "\t" + interface_name + "\t" + version +"\n" + "\n")
            #save_path.write(type_name + "\t" + self_name + "\t" + "\n")
        elif re.search('(.*?)\((.*?)\*(.*?)\)(.*?)\((.*?)\)(.*?)(.*?)',definition_str):
            ls = re.search('(.*?)\((.*?)\*(.*?)\)(.*?)\((.*?)\)(.*?)(.*?)',definition_str)
            type_name = ls.group(1) + "(*)(" + definition_str[definition_str.rfind(ls.group(5)): ]
            self_name = ls.group(3)
            type_name = "".join(type_name.split())
            self_name = "".join(self_name.split())
            save_path.write(type_name + "\t" + self_name + "\t" + interface_name + "\t" + version +"\n" + "\n")
            #save_path.write(type_name + "\t" + self_name + "\t" + "\n")
        else:
            split_pos = definition_str.rfind("\t")
            if(split_pos == -1):
                split_pos = definition_str.rfind(" ")
            type_name = definition_str[: split_pos]
            self_name = definition_str[split_pos: ]
            type_name = type_name.strip()
            self_name = self_name.strip()
            if self_name[0] == '*':
                self_name = self_name[1: ]
                type_name = type_name + "*"
            type_name = "".join(type_name.split())
            self_name = "".join(self_name.split())
            if(type_name.find("/*") >= 0):
                type_name = type_name[ :type_name.find("/*")]
            save_path.write(type_name + "\t" + self_name + "\t" + interface_name + "\t" + version +"\n" + "\n")
            #save_path.write(type_name + "\t" + self_name + "\t" + "\n")



def AnalysisLineToFindProperty(file_path, start_line, end_line, save_path, version):
	line = linecache.getline(file_path, start_line)
	start_pos = line.find('@interface')
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
	interface_name = line.strip()
	#save_path.write(file_path + "\n")
	#save_path.write(interface_name + "\n")
	#save_path.write(str(start_line) + "-----" + str(end_line) + "\n")
	line_count = start_line
	while line_count < end_line:
		temp_line = linecache.getline(file_path, line_count)
		if temp_line.find('@property') >= 0:
			#GetPropertyDefinition(temp_line, save_path, interface_name, line_count)
			GetProperty(temp_line, save_path, interface_name, version, line_count)
		line_count = line_count + 1;
	

def GetTargetDescription(file_path, save_path, version):
	file = open(file_path, 'r')
	line = file.readline()
	start_line = 1
	end_line = 1
	cur_line = 1
	start_target = '@interface'
	end_target = '@end'
	while line:
		if line.find(start_target) >= 0:
			start_line = cur_line
			while line:
				if line.find(end_target) >= 0:
					end_line = cur_line
					AnalysisLineToFindProperty(file_path, start_line, end_line, save_path, version)
					break
				line = file.readline()
				cur_line = cur_line + 1
		line = file.readline()
		cur_line = cur_line + 1


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
    print ("property:\n")
    for version_filepath in version_filepaths:
        target_filepath = os.path.join(root_filepath, version_filepath)
        if os.path.isdir(target_filepath):
            print (target_filepath)
            version_start = target_filepath.find('iPhoneOS')
            version_end = target_filepath.find('.sdk')
            version = target_filepath[version_start + 8 : version_end]
            save_name = "/Users/linjunhao/Desktop/complie_opt/TraversingOutput/property/" + target_filepath[version_start : version_end] + "_property.txt"
            fp = open(save_name, 'w')
            GetTargetFilePath(target_filepath, fp, version)
            fp.close()

