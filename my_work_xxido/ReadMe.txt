1、DataHandle_main：
用于对系统sdk进行检测，获得其中定义的接口与属性的相关信息，并将其入库
执行时，需确保数据库的开启

2、BuildOutputHandle_main：
将wework的编译日志存储至/Users/yuxingdong/备份/wework_test文件夹中，并命名为Build_output.txt
用于对clang匹配到的数据信息进行处理，生成接口信息文件和属性信息文件


3、APICheck_main：
将clang匹配到的数据信息与库中的数据信息进行对比，实现API检测
执行时，需确保数据库的开启

4、数据信息位于：
/Users/yuxingdong/TraversingOutput/

5、Find_Availability_main：
用于对Xcode自带检查生成的警告信息进行的处理