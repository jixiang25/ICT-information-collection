# ICT-information-collection
Collect text information from www.ict.ac.cn

## 执行方式
直接执行framework.py，即可得到需要的文件

## 各文件说明
data.txt 文本文件，每一行是一个json，包含一个str类型的title（网页的标题），一个str类型的url（网页的来源），以及一个list类型的paragraph（其中的元素都是str，每一个是一个自然段）

pdf_url.txt 站内全部pdf的url

url.txt 中间文件

collect_except_url.txt 一些无法直接采集的网页，包括跳转页面，doc文件，表单页面等
