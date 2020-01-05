1. HTML档描述
    - templates文件夹里的HTML档文件是使用jpyter notebook将17级制作完成的交互式可视化数据图文件的每个数据图分别导出为html格式所生成的。用于制作之后的数据故事。
    - afr.html和max_afr.html是2010年到2016年间世界各国青少年怀孕率地图，其中max_afr.html还含有青少年怀孕率最高和最低的条形图。
    - min_afr.html是1990年到2005年间芬兰和马里两国教育程度对比图。
    - search.html是Bahrain青少年生育率/国民生产总值GDP
    - story.html是数据故事的描述。
    - example1.html是以Aruba为例2的数据。
    - gdp.html是2010年到2016年间全球国家人均GDP地图，gdp_afp.html和gdp_pand_afp.html是青少年怀孕率最高八国的GDP和怀孕率的关系。


2. python档描述
    - 通过判断不同的查询地址跳转到不同地址的内容
    - 创建了HTML的表单发送到浏览器
    - 从flask呈现模板，导入对应函数创建一个新的url返回正确呈现的HTML
    - 通过代码与数据的交互实现不同功能


3. Web App动作描述
    - 点击数据故事会跳转到/story页面
    - 点击交互图源代码会跳转到/new页面
    - 点击Dash Tables会跳转到/dash页面
    - 选择下拉框里不同的国家和地区后，再点击do it就可以跳转到/search下不同国家和地区的数据图


4. [PythonAnywhere页面](http://lsm.pythonanywhere.com/)
