import os

file_path = r'C:\Users\YQ\Desktop\Code\dianwaimai-reminder\tests\test_reminder.py'
with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(f'第8行当前内容: {repr(lines[7])}')

# 修复：将5个右括号改为4个
old_line = lines[7]
if '__file__)))) ' in old_line:
    lines[7] = old_line.replace('__file__)))) ', '__file__)))) ')
    print(f'修复后: {repr(lines[7])}')
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    print('✓ 修复完成')
else:
    print('未找到预期模式，尝试直接修复...')
    # 直接修复：找到 __file__ 后面的 ))))) 并改为 )))))
    line = lines[7]
    idx = line.find('__file__')
    if idx != -1:
        after = line[idx + len('__file__'):]
        # 计算右括号数量
        count = 0
        for c in after:
            if c == ')':
                count += 1
            else:
                break
        print(f'__file__ 后有 {count} 个右括号')
        if count > 4:
            # 删除多余的右括号
            new_after = ')' * 4 + after[count:]
            lines[7] = line[:idx + len('__file__')] + new_after
            with open(file_path, 'w', encoding='utf-8') as f:
                f.writelines(lines)
            print(f'修复后: {repr(lines[7])}')
            print('✓ 修复完成（直接修复方式）')
