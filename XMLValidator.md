# XML Validator

A robust Python utility for validating XML files and checking their well-formedness with detailed error reporting.

## Features

- **Comprehensive Validation**: Checks XML syntax, tag balancing, attribute formatting, and character encoding
- **Detailed Error Reporting**: Provides line numbers, column positions, and specific error messages
- **Encoding Detection**: Automatically detects file encoding (UTF-8, UTF-8-SIG, Latin-1, etc.)
- **Professional Output**: Clean, actionable error reports with fix suggestions
- **Cross-Platform**: Works on Windows, macOS, and Linux
- **Exit Codes**: Proper return codes for scripting and automation

## Installation

No installation required - just download the script:

```bash
# Clone or download XMLValidator.py
wget https://github.com/KodeDevHub/xml-validator/main/XMLValidator.py
```

**Requirements:**
- Python 3.6 or higher
- No external dependencies (uses Python's built-in `xml.parsers.expat`)

## Usage

### Basic Validation

```bash
# Validate a single XML file
python XMLValidator.py document.xml

# With full path (handles spaces in paths)
python XMLValidator.py "C:\Users\username\My Documents\data.xml"
python XMLValidator.py "/home/user/projects/config.xml"
```

### Command-Line Options

The script accepts exactly one argument - the XML file to validate:

```bash
# Basic usage
python XMLValidator.py <xml_file>

# Examples
python XMLValidator.py data.xml
python XMLValidator.py "path with spaces/file.xml"
python XMLValidator.py ../configs/settings.xml
```

### Exit Codes

| Code | Meaning |
|------|---------|
| 0    | XML is valid and well-formed |
| 1    | XML contains syntax errors |
| 2    | File not found or unreadable |
| 130  | Validation interrupted by user (Ctrl+C) |

## Output Examples

### Valid XML

```
File: example.xml
Path: C:\Users\user\Documents
------------------------------------------------------------
Size: 428 bytes
Modified: 1706543200.0
Encoding detected: utf-8-sig
Content length: 428 characters
------------------------------------------------------------
✓ XML is valid and well-formed.

✓ VALIDATION SUCCESSFUL
  Document lines: 15
  XML elements: 8
  XML declaration: Present
```

### Invalid XML

```
File: broken.xml
Path: C:\Users\user\Documents
------------------------------------------------------------
Size: 256 bytes
Modified: 1706543100.0
Encoding detected: utf-8
Content length: 256 characters
------------------------------------------------------------
✗ XML VALIDATION ERRORS
============================================================

ERROR 1:
  Type:    Tag mismatch: Expected </title>
  Line:    4
  Column:  15
  Context: title

ERROR 2:
  Type:    Malformed attribute (missing quotes)
  Line:    3
  Column:  20
  Context: product

============================================================

✗ VALIDATION FAILED
  Error count: 2
```

## Error Types Detected

The validator detects and reports:

- **Syntax errors**: Malformed XML structure
- **Tag mismatches**: Unclosed or mismatched tags
- **Attribute errors**: Missing quotes, duplicate attributes
- **Character encoding issues**: Invalid UTF-8 sequences
- **Namespace errors**: Unbound prefixes, undeclared namespaces
- **Entity errors**: Undefined entities, bad character references
- **Well-formedness issues**: Multiple root elements, content after root

## Integration

### Use in Scripts

```bash
#!/bin/bash
# Validate XML and act on result
python XMLValidator.py config.xml

if [ $? -eq 0 ]; then
    echo "XML is valid - proceeding with deployment"
    # Continue with your script
else
    echo "XML validation failed - aborting"
    exit 1
fi
```

### Use in Python Code

```python
from XMLValidator import XMLValidator, validate_xml_file

# Option 1: Use the high-level function
result = validate_xml_file('data.xml')
if result:
    print("Validation successful")
else:
    print("Validation failed")

# Option 2: Use the validator class directly
validator = XMLValidator()
with open('data.xml', 'r', encoding='utf-8') as f:
    content = f.read()

if validator.validate(content):
    print("XML is valid")
else:
    print("Errors found:")
    print(validator.get_error_report())
```

## Technical Details

### Supported Encodings

The validator attempts to read files with these encodings (in order):
1. UTF-8 with BOM (`utf-8-sig`)
2. UTF-8
3. Latin-1 (`iso-8859-1`)
4. Windows-1252 (`cp1252`)
5. Fallback: UTF-8 with error replacement

### XML Standards Compliance

- XML 1.0 specification
- Well-formedness constraints
- Character encoding compliance
- Namespace well-formedness
- Entity reference validation

### Performance

- Memory efficient: Processes files incrementally
- Fast validation: Uses Python's native expat parser
- Scalable: Handles files from kilobytes to gigabytes

## Troubleshooting

### Common Issues

1. **"File does not exist"**: Check file path and permissions
2. **Encoding errors**: Ensure file is saved with proper encoding (UTF-8 recommended)
3. **Permission denied**: Check file and directory permissions
4. **No output**: File might be empty or contain only whitespace

### Debug Mode

For detailed debugging, modify the script to add:

```python
import traceback
try:
    # validation code
except Exception as e:
    traceback.print_exc()
```

## Examples

### Sample XML Files

**Valid XML Example:**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<library>
    <book id="1">
        <title>Python Programming</title>
        <author>John Smith</author>
        <year>2023</year>
        <price currency="USD">39.99</price>
    </book>
    <book id="2">
        <title>XML Fundamentals</title>
        <author>Jane Doe</author>
        <year>2022</year>
        <price currency="EUR">29.50</price>
    </book>
</library>
```

**Invalid XML Example:**
```xml
<?xml version="1.0"?>
<products>
    <product id=101>  <!-- ERROR: Missing quotes -->
        <name>Laptop</name>
        <price>999.99</price>
    <!-- ERROR: Missing closing comment -->
</products>
```

## License

This project is provided as-is for educational and practical use. No warranty is provided.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## Support

For issues, feature requests, or questions:
- Open an issue on GitHub
- Ensure you include the XML file causing the problem
- Provide Python version and operating system details