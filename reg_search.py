import re

def reg_search(text, regex_list):
    result = []
    # 遍历正则规则列表（示例中是单元素列表，所以最终返回单元素结果）
    for regex_dict in regex_list:
        item = {}
        for field, pattern in regex_dict.items():
            # 根据字段名定制处理逻辑（结合示例需求设计）
            if field == "标的证券":
                # 匹配股票代码（6位数字+.+2位字母，如600900.SH）
                code_match = re.search(r'(\d{6}\.[A-Za-z]{2})', text)
                item[field] = code_match.group(1) if code_match else None
            
            elif field == "换股期限":
                # 匹配日期（xxxx 年 x 月 x 日），支持提取多个日期
                date_matches = re.findall(r'(\d{4}) 年 (\d{1,2}) 月 (\d{1,2}) 日', text)
                # 格式化日期为 YYYY-MM-DD（补全前置零）
                formatted_dates = []
                for year, month, day in date_matches:
                    formatted = f"{year}-{int(month):02d}-{int(day):02d}"
                    formatted_dates.append(formatted)
                item[field] = formatted_dates if formatted_dates else None
            
            else:
                # 通用匹配逻辑（适用于其他字段）
                matches = re.findall(pattern, text)
                item[field] = matches if matches else None
        
        result.append(item)
    return result

# 测试
if __name__ == "__main__":
    text = '''
标的证券：本期发行的证券为可交换为发行人所持中国长江电力股份
有限公司股票（股票代码：600900.SH，股票简称：长江电力）的可交换公司债
券。
换股期限：本期可交换公司债券换股期限自可交换公司债券发行结束
之日满 12 个月后的第一个交易日起至可交换债券到期日止，即 2023 年 6 月 2
日至 2027 年 6 月 1 日止。
    '''
    
    # 正则规则列表
    regex_list = [
        {
            '标的证券': '',
            '换股期限': ''
        }
    ]
    
    # 调用函数并打印结果
    print(reg_search(text, regex_list))