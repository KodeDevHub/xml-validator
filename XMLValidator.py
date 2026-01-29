from xml.parsers.expat import ParserCreate, ExpatError
import os
import sys

class XMLValidator:
    def __init__(self):
        self.parser = ParserCreate()
        self.errors = []
        
        # Store reference to self for error handler closure
        self_ = self
        
        # Define error handler as inner function to capture self reference
        def expat_error_handler(code, message, line, column, context):
            # Handle byte strings safely
            if isinstance(message, bytes):
                message = message.decode('utf-8', 'ignore')
            if isinstance(context, bytes):
                context = context.decode('utf-8', 'ignore')
            
            self_._record_error(code, message, line, column, context)
        
        # Try different approaches for error handler assignment
        try:
            # Modern Python versions
            self.parser.ErrorHandler = expat_error_handler
        except AttributeError:
            try:
                # Alternative attribute name
                self.parser.error_handler = expat_error_handler
            except AttributeError:
                # If no error handler attribute exists, we'll catch errors in Parse method
                pass
    
    def _record_error(self, code, message, line, column, context):
        """Record parser error with context"""
        # Map error codes to human-readable messages
        # We'll use a subset of common errors to avoid version-specific constants
        error_descriptions = {
            1: "Syntax error",
            2: "No elements found",
            3: "Invalid token",
            4: "Unclosed token",
            5: "Partial character",
            6: "Tag mismatch",
            7: "Duplicate attribute",
            8: "Junk after document element",
            9: "Parameter entity reference",
            10: "Undefined entity",
            11: "Recursive entity reference",
            12: "Async entity",
            13: "Bad character reference",
            14: "Binary entity reference",
            16: "Attribute external entity",
            17: "Misplaced XML PI",
            18: "Unknown encoding",
            19: "Incorrect encoding",
            20: "Unclosed CDATA section",
            21: "External entity handling",
            22: "Not standalone",
            23: "Unexpected state",
            24: "Entity in PE",
            25: "Feature requires DTD",
            26: "Cannot change feature",
            27: "Unbound prefix",
            28: "Undeclaring prefix",
            29: "Incomplete PE",
            30: "XML declaration",
            31: "Text declaration",
            32: "Public ID",
            33: "Suspended",
            34: "Not suspended",
            35: "Aborted",
            36: "Finished",
            37: "Suspended PE"
        }
        
        error_msg = error_descriptions.get(code, f"XML error {code}")
        if message and message != error_msg:
            full_message = f"{error_msg}: {message}"
        else:
            full_message = error_msg
        
        self.errors.append({
            'code': code,
            'message': full_message,
            'line': line,
            'column': column,
            'context': context or "Unknown"
        })
    
    def validate(self, xml_string):
        """Validate XML string, return True if well-formed"""
        try:
            # Clear previous errors
            self.errors.clear()
            
            # Parse the XML
            self.parser.Parse(xml_string, True)
            
            # Check if we collected any errors
            if self.errors:
                return False
            
            return True
            
        except ExpatError as e:
            # If parse fails with exception, capture it
            # Check if we have the error code attribute
            error_code = getattr(e, 'code', 0)
            
            # Only add if not already captured by error handler
            if not self.errors:
                self._record_error(
                    error_code, 
                    str(e), 
                    getattr(e, 'lineno', 0), 
                    getattr(e, 'offset', 0), 
                    'ExpatError'
                )
            return False
        except Exception as e:
            # Catch any other exceptions
            self.errors.append({
                'code': -1,
                'message': f"Parser exception: {str(e)}",
                'line': 0,
                'column': 0,
                'context': 'Parser'
            })
            return False
    
    def get_error_report(self):
        """Generate formatted error report"""
        if not self.errors:
            return "✓ XML is valid and well-formed."
        
        report = []
        report.append("✗ XML VALIDATION ERRORS")
        report.append("=" * 60)
        
        for i, error in enumerate(self.errors, 1):
            report.append(f"\nERROR {i}:")
            report.append(f"  Type:    {error['message']}")
            if error['line'] > 0:
                report.append(f"  Line:    {error['line']}")
            if error['column'] > 0:
                report.append(f"  Column:  {error['column']}")
            if error['context'] and error['context'] not in ['Unknown', 'Parser', 'ExpatError']:
                report.append(f"  Context: {error['context']}")
        
        report.append("\n" + "=" * 60)
        return "\n".join(report)

def read_xml_file(filepath):
    """Read XML file with encoding detection"""
    encodings = ['utf-8-sig', 'utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
    
    for encoding in encodings:
        try:
            with open(filepath, 'r', encoding=encoding) as f:
                return f.read(), encoding
        except UnicodeDecodeError:
            continue
    
    # Final attempt: binary read with utf-8 ignore
    try:
        with open(filepath, 'rb') as f:
            content = f.read()
            return content.decode('utf-8', errors='ignore'), 'utf-8 (lossy)'
    except Exception:
        return None, None

def validate_xml_file(file_path):
    """Validate XML file and print results"""
    print(f"File: {os.path.basename(file_path)}")
    print(f"Path: {os.path.dirname(file_path)}")
    print("-" * 60)
    
    if not os.path.exists(file_path):
        print("✗ File does not exist")
        return False
    
    try:
        file_stats = os.stat(file_path)
        print(f"Size: {file_stats.st_size:,} bytes")
    except OSError:
        print("✗ Cannot access file metadata")
        return False
    
    content, encoding = read_xml_file(file_path)
    if content is None:
        print("✗ Cannot read file (encoding issue or file corruption)")
        return False
    
    print(f"Encoding detected: {encoding}")
    print(f"Content length: {len(content):,} characters")
    print("-" * 60)
    
    validator = XMLValidator()
    is_valid = validator.validate(content)
    
    print(validator.get_error_report())
    
    if is_valid:
        # Basic XML statistics
        lines = content.count('\n') + 1
        # Count approximate element tags (excluding declarations and comments)
        tags = content.count('<') - content.count('<?') - content.count('<!')
        print(f"\n✓ VALIDATION SUCCESSFUL")
        print(f"  Document lines: {lines}")
        print(f"  XML elements: {tags}")
        if '<?xml' in content[:100]:
            print(f"  XML declaration: Present")
    else:
        print(f"\n✗ VALIDATION FAILED")
        print(f"  Error count: {len(validator.errors)}")
    
    return is_valid

def main():
    """Command line entry point"""
    if len(sys.argv) != 2:
        script_name = os.path.basename(sys.argv[0])
        print(f"XML Validator - Validate XML file structure")
        print()
        print(f"Usage: {script_name} <xml_file>")
        print()
        print(f"Example: {script_name} document.xml")
        print(f"Example: {script_name} \"file with spaces.xml\"")
        return 1
    
    file_path = sys.argv[1]
    
    try:
        is_valid = validate_xml_file(file_path)
        return 0 if is_valid else 1
    except KeyboardInterrupt:
        print("\n✗ Validation interrupted by user")
        return 130
    except Exception as e:
        print(f"\n✗ Critical error: {e}")
        # For debugging
        import traceback
        traceback.print_exc()
        return 2

if __name__ == "__main__":
    sys.exit(main())