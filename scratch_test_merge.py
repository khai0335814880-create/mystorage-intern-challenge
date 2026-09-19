import pypdf
import os

cv_file = r'd:\HK1_2627\WEBnangcao\mystorage-intern-challenge\CV_AI_ProductManage_EN.pdf'
output_file = r'd:\HK1_2627\WEBnangcao\mystorage-intern-challenge\test_merged.pdf'

writer = pypdf.PdfWriter()
writer.append(cv_file)
with open(output_file, 'wb') as f:
    writer.write(f)

print('Successfully merged PDF using PdfWriter! Size:', os.path.getsize(output_file), 'bytes')
