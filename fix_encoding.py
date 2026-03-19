import chardet

def detect_and_fix(file_path):
    with open(file_path, 'rb') as f:
        raw_data = f.read()
    
    result = chardet.detect(raw_data)
    encoding = result['encoding']
    print(f"Detected encoding: {encoding} with confidence {result['confidence']}")
    
    if encoding and encoding.lower() != 'utf-8':
        try:
            content = raw_data.decode(encoding)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print("Successfully converted to UTF-8")
        except Exception as e:
            print(f"Failed to convert: {e}")
    else:
        print("File is already UTF-8 or unknown")

if __name__ == "__main__":
    detect_and_fix(r"e:\Project_Personal\xianyu_project\xianyu-auto-reply-main\xianyu-auto-reply-main\XianyuAutoAsync.py")
