## PHP Backdoor Scan ##
_基于语义分析的php后门扫描_

感谢23hush同学，感谢CFC4N同学，感谢衰仔同学，感谢Sawako同学，感谢secsay的所有同学，感谢人人网MVP，感谢国家
低调发布一个测试版本，目前不开放插件模式，目前暂不支持xss扫描和SQL注入扫描

## 特点 ##
基于语义分析，能有效识别类似下面的后门方式，可自写插件进行特定类型分析。
```
    $aa=$_GET['test'];
    $aa($bbb);
    $_POST[f]($_POST[c]);
    $data=$_POST[c];
    eval($data);
```
## 使用说明 ##

两个程序都只扫描目录中的php和inc文件。

### php\_shell\_scan.exe ###
采用语义分析的方法进行后门检测，分严谨扫描模式和深度探索模式。
日志添加在程序目录下scan.log中
#### 严谨扫描模式 ####
```
	php_shell_scan.exe dir
	php_shell_scan.exe file
```
#### 深度探索模式 ####
```
	php_shell_scan.exe dir maybe
	php_shell_scan.exe file maybe
```

### php\_shell\_scan\_re.exe ###
基于正则表达式，需要较多人工干预
日志添加在程序目录下relog.log中
用法：
```
	php_shell_scan_re.exe dir
```